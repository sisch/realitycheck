from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns('',
    url(r'^getNextPost/(?P<id>\d+)/$', views.get_next_three_posts, name='getNextPost'),
    url(r'^api/posts/bytime/(?P<timestamp>\d+)/$', views.post_detail, name='postDetailByTime'),
    url(r'^api/posts/(?P<id>\d+)/$', views.post_detail, name='postDetailByID'),
    url(r'^$', views.index, name="index"),
)
