from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns('',
    url(r'^getNextPost/(?P<id>\d+).*$', views.get_next_post, name='getNextPost'),
    url(r'^.*$', views.index, name="index"),
)
