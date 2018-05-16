# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context_processors import csrf
from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。

from .forms import UserForm
from swiftclient import *

from django.http import StreamingHttpResponse

import os

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

# def index(request):
#     auth = get_auth()
#     return render(request,'index.html',{'auth':auth})

_authurl = 'http://swift_node:5000/v3/'
_auth_version = '3'
_user = 'admin'
_key = 'lj0609'
_os_options = {
        'user_domain_name': 'Default',
        'project_domain_name': 'Default',
        'project_name': 'admin'
    }
    
def get_auth():
    _authurl = 'http://swift_node:5000/v3/'
    _auth_version = '3'
    _user = 'admin'
    _key = 'lj0609'
    _os_options = {
        'user_domain_name': 'Default',
        'project_domain_name': 'Default',
        'project_name': 'admin'
    }
    conn = Connection(
        authurl=_authurl,
        user=_user,
        key=_key,
        os_options=_os_options,
        auth_version=_auth_version
    )
    return conn
    
#登录后的首页，打印所有容器    
def index(request):
    conn = get_auth()
    resp_headers, containers = conn.get_account()
    container1 = []
    for container in containers:
        container1.append('{}'.format(container['name']))
        container2 = list(set(container1)) 
    conn.close()
    return render(request,'index.html',{'container':container2})
     


def get_object_views(request):
    container = request.GET['container'].replace('/','')
    if request.method=="POST":  
        handle_upload_file(container,request.FILES['file'],str(request.FILES['file']))          
        #return HttpResponse('Successful') #此处简单返回一个成功的消息，在实际应用中可以返回到指定的页面中
    if request.method=="GET":
        if request.GET.get('download'):
            container = request.GET['container'].replace('/','')
            filename = request.GET['object'].replace('/','')
            handle_download_file(container,filename)
        if request.GET.get('delete'):
            container = request.GET['container'].replace('/','')
            filename = request.GET['object'].replace('/','')
            handle_delete_object(container,filename)

    conn = get_auth()
    #打印指定容器中所有对象的名字大小时间
    auth = []
    bytes = []
    Last_Modified = []
    for data in conn.get_container(container)[1]:
        auth.append('{}'.format(data['name']))
        bytes.append('{}'.format(data['bytes']))
        Last_Modified.append('{}'.format(data['last_modified']))
    return render(request,'get_object_views.html',{'auth':auth,'container':container,'bytes':bytes,'Last_Modified':Last_Modified})

#上传文件
def handle_upload_file(container,file,filename):  
    path='media/uploads/'     #上传文件的保存路径，可以自己指定任意的路径  
    if not os.path.exists(path):  
        os.makedirs(path)  
    with open(path+filename,'wb+')as destination:  
        for chunk in file.chunks():  
            destination.write(chunk)
    conn = get_auth()
    with open(path+filename, 'r') as local:
        conn.put_object(
            container,
            filename,
            contents=local,
            content_type='text/plain'
            )

#下载文件
def handle_download_file(container,filename):
    path='media/downloads/'
    if not os.path.exists(path):  
        os.makedirs(path)
    
    conn = get_auth()
    resp_headers, obj_contents = conn.get_object(container, filename)
    with open(path+filename, 'w') as local:
        local.write(obj_contents)
    
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
    return response

#删除对象
def handle_delete_object(container,filename):
    conn = get_auth()
    conn.delete_object(container, filename)
    
#获取对象内容
def get_object_body_views(request):
    container = request.GET['container'].replace('/','')
    id = request.GET['object'].replace('/','')
    conn = Connection(
        authurl=_authurl,
        user=_user,
        key=_key,
        os_options=_os_options,
        auth_version=_auth_version
    )
    #打印指定容器中所有对象的名字大小时间
    obj_header, obj_body = conn.get_object(container,id)
    return render(request,'get_object_body_views.html',{'obj_body':obj_body})

#注册
def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 判断用户是否存在
            user = auth.authenticate(username = username,password = password)
            if user:
                context['userExit']=True
                return render(req, 'register.html', context)


            #添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username=username, password=password)
            user.save()

            #添加到session
            req.session['username'] = username
            #调用auth登录
            auth.login(req, user)
            
            conn = get_auth()
            container = username
            conn.put_container(container)
            resp_headers, containers = conn.get_account()
            if container in containers:
                print("The container was created")
            #重定向到首页
            return redirect('/get_object_views/?container=%s'% username)
    else:
        context = {'isLogin':False}
    #将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return  render(req,'register.html',context)

#登录
def login_view(request):
    context = {}
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #获取表单用户密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #获取的表单数据与数据库进行比较
            user = authenticate(username = username,password = password)
            if user:
                #比较成功，跳转index
                auth.login(request,user)
                request.session['username'] = username
                return redirect('/get_object_views/?container=%s'% username)
            else:
                #比较失败，还在login
                context = {'isLogin': False,'pawd':False}
                return render(request, 'login.html', context)
    else:
        context = {'isLogin': False,'pswd':True}
    return render(request, 'login.html', context)

#登出    
def logout_view(req):
    #清理cookie里保存username
    auth.logout(req)
    return redirect('/login/')
