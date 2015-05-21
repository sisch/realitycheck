from django.shortcuts import render
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import feedgenerator
from blog.models import Post
import datetime

def index(request):
    post_list = Post.objects.order_by('-pub_date')[:5]
    template = loader.get_template('blog/template.html')
    context = RequestContext(request, {
        'post_list': post_list,
        'index' : True,
        'more_button': True,
        'home': True,
        'load_flattr': False,
    })
    return HttpResponse(template.render(context))

def get_next(request, timestamp):
    dt = datetime.datetime.fromtimestamp(float(timestamp))
    post_list = Post.objects.all().filter(pub_date__lte=dt).filter(hidden=False).order_by('-pub_date')[1:2]
    template = loader.get_template('blog/template.html')
    context = RequestContext(request, {
        'post_list': post_list,
        'index' : False,
        'more_button': False,
        'home': False,
        'load_flattr': True,
    })
    return HttpResponse(template.render(context))

def atom_feed(request):
    dt = datetime.datetime.now()
    post_list = Post.objects.all().filter(pub_date__lte=dt).filter(hidden=False).order_by('-pub_date')
    lastPost = post_list[0].pub_date
    template = loader.get_template('blog/feed.html')
    context = RequestContext(request, {
        'post_list': post_list,
        'datetime': lastPost,
        })
    return HttpResponse(template.render(context))

def post_detail(request, **kwargs):
    post_list = None
    if "id" in kwargs:
        # -1 offset, because ids are 1-indexed in rendered HTML file
        id = max(int(kwargs["id"]) - 1, 0)
        post_list = Post.objects.order_by('pub_date')[int(id):int(id)+1]
    elif "timestamp" in kwargs:
        key = kwargs["timestamp"]
        dt = datetime.datetime.fromtimestamp(float(key))
        post_list = Post.objects.all().filter(pub_date__gte=dt)[0:1] # pub_date=dt)
    template = loader.get_template('blog/template.html')
    context = RequestContext(request, {
        'post_list': post_list,
        'index' : True,
        'more_button': False,
        'home': True,
        'load_flattr': False,
    })
    return HttpResponse(template.render(context))