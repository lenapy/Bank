from django.conf.urls import url

from bank.blog import views

urlpatterns = [

    url(r'^new/$', views.blog_new, name='new'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.blog_edit, name='edit'),
    url(r'^(?P<pk>[0-9]+)/del/$', views.blog_del, name='del'),
    url(r'^all/$', views.blog_all, name='all')
]