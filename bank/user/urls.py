from django.conf.urls import url

from bank.user import views

urlpatterns = [

    url(r'^registration/$', views.registration, name='registration'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^change_password/$', views.change_password, name='change_password'),
    url(r'^profile/$', views.profile, name='profile'),

]