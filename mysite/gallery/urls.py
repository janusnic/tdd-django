from django.conf.urls import patterns, include, url
from .views import ItemsListView, ItemObjectView, PhotoObjectView , ItemObjectView

urlpatterns = [
    url(r'^$', ItemsListView.as_view(), name="item_list"),
    
    url(r'^(?P<pk>\d+)/$', ItemObjectView.as_view(), name="item_object"),
    url(r'^photo/(?P<pk>\d+)/$', PhotoObjectView.as_view(), name="photo_object")
]