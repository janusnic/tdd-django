# example/simple/urls.py

from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    
    url(r'^$', views.home_page, name='home'),
    #url(r'^login/(\w*)', views.login, name='login')
)