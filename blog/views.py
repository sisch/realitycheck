from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect
from blog.models import Post
from itertools import chain
import datetime
import django.utils.timezone as timezone
import time
import random

def index(request):
    dt = timezone.now()

    post_list = Post.objects.order_by('-pub_date').filter(pub_date__lte=dt).filter(visible=True)[:5]
    template = get_template('blog/template.html')
    context = {
        'post_list': post_list,
        'index' : True,
        'more_button': True,
        'home': True,
        'load_flattr': False,
        'active_page': 'index',
	'canonical_suffix': '',
    }
    return HttpResponse(template.render(context, request))


def get_next(request, timestamp):
    dt = timezone.make_aware(timezone.datetime.fromtimestamp(float(timestamp)), timezone=timezone.get_current_timezone())
    post_list = Post.objects.all().filter(pub_date__lte=dt).filter(visible=True).order_by('-pub_date')[1:2]
    template = get_template('blog/template.html')
    context = {
        'post_list': post_list,
        'index' : False,
        'more_button': False,
        'home': False,
        'load_flattr': True,
    }
    return HttpResponse(template.render(context,request))


def atom_feed(request):
    dt = timezone.now()
    post_list = Post.objects.all().filter(pub_date__lte=dt).filter(visible=True).order_by('-pub_date')[0:20]
    lastPost = post_list[0].pub_date
    template = get_template('blog/feed.html')
    context = {
        'post_list': post_list,
        'datetime': lastPost,
        }
    return HttpResponse(template.render(context, request))


def post_random(request):
    return post_detail(request, random=True)


def post_detail(request, **kwargs):
    single_post = None
    now = timezone.now()
    active_menu_entry = ''
    if "id" in kwargs:
        # -1 offset, because ids are 1-indexed in rendered HTML file
        id = max(int(kwargs["id"]) - 1, 0)
        single_post = Post.objects.order_by('pub_date')[int(id):int(id)+1]
    elif "timestamp" in kwargs:
        key = kwargs["timestamp"]
        dt = datetime.datetime.fromtimestamp(float(key))
        single_post = Post.objects.all().filter(pub_date__gte=dt)[0:1] # pub_date=dt)
    elif "random" in kwargs:
        ids = Post.objects.all().values_list('id', flat=True)
        random_id = random.choice(list(ids))
        single_post = Post.objects.filter(id=random_id)
        active_menu_entry = 'random'
    post_list = Post.objects.all().filter(visible=True).filter(pub_date__lte=now).exclude(pub_date__exact=single_post.values()[0]['pub_date']).order_by('-pub_date')[:4]
    post_list = chain(single_post, post_list)

    twitter_description = single_post.values()[0]['reality']
    canonical_suffix = "{}/".format(int(time.mktime(single_post.values()[0]['pub_date'].timetuple())+3600))
    twitter_card = {
            'title': single_post.values()[0]['title'],
            'description': twitter_description[:100] + ("..." if len(twitter_description) > 100 else "")
    }
    if "random" in kwargs:
        canonical_suffix = "post/random/"
        twitter_card = {
            'title': "random post",
            'description': "... surprise ..."
        }
    template = get_template('blog/template.html')
    context = {
        'post_list': post_list,
        'twitter_card': twitter_card,
        'detail': True,
        'index': True,
        'more_button': True,
        'home': True,
        'load_flattr': False,
        'active_page': active_menu_entry,
        'canonical_suffix': canonical_suffix,
    }
    return HttpResponse(template.render(context, request))


def search(request, **kwargs):
    if 'q' in request.GET:
        searchterm = request.GET['q']
        post_list = Post.objects.filter(Q(title__icontains=searchterm) | \
            Q(reality__icontains=searchterm) | \
            Q(story__icontains=searchterm))
        template = get_template('blog/template.html')
        canonical_suffix = ""
        if len(post_list)>0:
            canonical_suffix = "{}/".format(int(time.mktime(post_list.values()[0]['pub_date'].timetuple())+3600))
        context = {
            'post_list': post_list,
            'detail': False,
            'index': True,
            'more_button': False,
            'home': False,
            'load_flattr': True,
            'active_page': 'search',
            'searchterm': searchterm,
            'canonical_suffix': canonical_suffix,
        }
        return HttpResponse(template.render(context, request))
    return redirect('postRandom')


def sitemap(request):
    dt = timezone.now()
    post_list = Post.objects.order_by('-pub_date').filter(pub_date__lte=dt).filter(visible=True)
    template = get_template('blog/sitemap.html')
    context = {'post_list': post_list}
    return HttpResponse(template.render(context, request))


def contact(request):
    template = get_template('blog/template.html')
    context = {'active_page': 'imprint','index':True,'canonical_suffix': 'impressum/'}
    return HttpResponse(template.render(context, request))
