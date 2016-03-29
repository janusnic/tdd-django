"""shop URL Configuration


"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<id>\d+)/$', views.product_detail, name='product_detail'),
]
