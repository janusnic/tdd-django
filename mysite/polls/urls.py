from django.conf.urls import patterns, include, url


from polls.views import Home, Detail

urlpatterns = [
    url(r'^$', Home.as_view(), name='home'),
    url(r'^poll/(?P<pk>\d+)/$', Detail.as_view(), name='polls-detail'),
 
]
