from django.conf.urls import url

from bank.blog import views

urlpatterns = [

    url(r'^new/$', views.blog_new, name='new'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.blog_edit, name='edit'),
    url(r'^(?P<pk>[0-9]+)/del/$', views.blog_del, name='del'),
    url(r'^(?P<pk>[0-9]+)/comment-new/$', views.comment_new, name='comment_new'),
    url(r'^(?P<pk_post>[0-9]+)/reply-to/(?P<pk_comment>[0-9]+)/$', views.reply_to_comment,
        name='reply'),
    url(r'^(?P<pk>[0-9]+)/del-comment/$', views.comment_del, name='del_comment'),
    url(r'^all/$', views.blog_all, name='all')
]