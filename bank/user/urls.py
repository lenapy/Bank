from django.conf.urls import url

from bank.user import views

urlpatterns = [

    url(r'^registration/$', views.registration, name='registration'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/upload_photo$', views.upload_photo, name='upload_photo'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.user_edit, name='edit'),
    url(r'^add_info/(?P<pk>[0-9]+)/$', views.user_add_info, name='add_about'),

]