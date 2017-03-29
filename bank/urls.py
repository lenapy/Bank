from django.conf.urls import url, include
from django.contrib import admin

from bank import views
from bank.user import urls as user_urls
from bank.achievement import urls as ach_urls

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/', include(user_urls, namespace='user')),
    url(r'^achievement/', include(ach_urls, namespace='achievement')),
    url(r'^admin/', include(admin.site.urls))


]
