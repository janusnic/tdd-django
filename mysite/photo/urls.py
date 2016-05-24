from django.conf.urls import url

from . import views

from .views import album, photo

urlpatterns = [
    
    url(r'^albums/$', album.list, name='albums'),
    url(r'^albums/(?P<pk>\d+)/$', album.detail, name='album'),
    url(r'^photos/(?P<pk>\d+)/$', photo.detail, name='photodetail'),

]
