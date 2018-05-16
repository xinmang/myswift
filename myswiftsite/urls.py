from django.conf.urls import url
from myswiftsite import views

urlpatterns = (
    url(r'^$', views.index),
    url(r'^get_object_views/$', views.get_object_views, name='handle_download_file'),
    url(r'^get_object_body_views/$', views.get_object_body_views),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view),
    url(r'^register/$', views.register_view, name='register'),
)
