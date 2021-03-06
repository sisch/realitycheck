from django.conf.urls import url

from blog import views

urlpatterns = [
    url(r'^api/posts/bytime/(?P<timestamp>\d+)/$', views.post_detail, name='postDetailByTime'),
    url(r'^api/posts/getNext/(?P<timestamp>\d+)/$', views.get_next, name='getNext'),
    url(r'^api/posts/(?P<id>\d+)/$', views.post_detail, name='postDetailByID'),
    url(r'^post/(?P<timestamp>\d+)/$', views.post_detail, name='postDetailTimestamp'),
    url(r'^post/random/$', views.post_random, name='postRandom'),
    url(r'^post/totally-not-random/$', views.post_random, name='postRandom2'),
    url(r'^feed(?:.xml)?/?$', views.atom_feed, name='feed'),
    url(r'^impressum/$', views.contact, name="imprint"),
    url(r'^sitemap(?:.txt)?/?$', views.sitemap, name="sitemap"),
    url(r'^search/$', views.search, name="search"),
    url(r'^$', views.index, name="index"),
]
