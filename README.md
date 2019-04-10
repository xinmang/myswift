## Myswift
Realization of Network Disk Function by Calling Swift API + Django

### Design Ideas
1. Because of the design and implementation of the network disk based on swift, a complete swift environment is needed first. Install the configuration keystone, and then install swift.

2. Find the API interface provided by swift. Familiar with the API of swiftclient and keystoneclient.

3. The container object of swift is operated by interface. Before getting authentication, check the username and password in the configuration file.

4. Django debugging, interface beautification.

### Establishment of project documents

1. Create an engineering file called myswift.
```django-admin.py startproject myswift```

2. Create an app called myswiftsite.
```django-admin.py startapp myswiftsite```

3. Modify settings files, modify them according to their own needs, and add MEDIA paths as transit stations for object upload and download.

### User Management
Designing the database needed for the implementation of this project, using Django's user module, verifying the registration and login, and setting the user's rights.


### Implementing Functions

1. User login registration

2. Object upload, download, edit and delete


## myswift
通过调用 swift api + Django 实现网盘功能

### 设计思路
1. 由于是基于swift的网盘设计与实现，首先需要完整的swift环境。安装配置keystone，然后安装swift。
2. 查找swift提供的api接口。熟悉swiftclient和keystoneclient的API的使用方法。
3. 利用接口对swift的容器对象进行操作。在此之前需获得认证，先查看配置文件中的用户名和密码。
4. Django的调试，界面的美化。

### 建立项目文件
1. 建立一个名叫myswift的工程文件。
```django-admin.py startproject myswift```
2. 建立一个名叫myswiftsite的app.
```django-admin.py startapp myswiftsite```
3. 修改settings文件，按照自己的需求修改，添加MEDIA路径，作为对象上传和下载的中转站。

### 用户管理
设计该项目实现所需要的数据库，使用Django自带的用户模块，进行注册登录的验证，以及设置用户的权限。


### 实现功能
1. 用户登录 注册
2. 对象上传 下载 编辑 删除

