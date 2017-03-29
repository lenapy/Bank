from django.conf.urls import url

from bank.achievement import views

urlpatterns = [

    url(r'^new/$', views.achievement_new, name='new'),
    url(r'^card/new/$', views.card_new, name='card_new'),
    url(r'^(?P<pk>[0-9]+)/card/edit/$', views.card_edit, name='card_edit'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.achievement_edit, name='edit'),


]


