from django.template import RequestContext, loader
from django.http import HttpResponse
from blog.models import Post
from itertools import chain
import datetime
import random


def index(request):
    dt = datetime.datetime.now()
    post_list = Post.objects.order_by('-pub_date').filter(pub_date__lte=dt).filter(visible=True)[:5]
    template = loader.get_template('blog/template.html')
    context = RequestContext(request, {
        'post_list': post_list,
        'index' : True,
        'more_button': True,
        'home': True,
        'load_flattr': False,
        'active_page': 'index',
    })
    return HttpResponse(template.render(context))


def get_next(request, timestamp):
    dt = datetime.datetime.fromtimestamp(float(timestamp))
    post_list = Post.objects.all().filter(pub_date__lte=dt).filter(visible=True).order_by('-pub_date')[1:2]
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
    post_list = Post.objects.all().filter(pub_date__lte=dt).filter(visible=True).order_by('-pub_date')[0:20]
    lastPost = post_list[0].pub_date
    template = loader.get_template('blog/feed.html')
    context = RequestContext(request, {
        'post_list': post_list,
        'datetime': lastPost,
        })
    return HttpResponse(template.render(context))


def post_random(request):
    return post_detail(request, random=True)


def post_detail(request, **kwargs):
    single_post = None
    now = datetime.datetime.now()
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

    template = loader.get_template('blog/template.html')
    context = RequestContext(request, {
        'post_list': post_list,
        'twitter_card': {
            'title': single_post.values()[0]['title'],
            'description': twitter_description[:100] + ("..." if len(twitter_description) > 100 else "")},
        'detail': True,
        'index': True,
        'more_button': True,
        'home': True,
        'load_flattr': False,
        'active_page': active_menu_entry,
    })
    return HttpResponse(template.render(context))


def search(request, **kwargs):
    if 'searchterm' in kwargs:
        searchterm = kwargs.get('searchterm','')
        from django.db.models import Q
        print(kwargs['searchterm'])
        post_list = Post.objects.filter(title__search=searchterm) | \
            Post.objects.filter(reality__search=searchterm) | \
            Post.objects.filter(story__search=searchterm)
        template = loader.get_template('blog/template.html')
        context = RequestContext(
            request, {
            'post_list': post_list,
            'detail': False,
            'index': True,
            'more_button': False,
            'home': False,
            'load_flattr': True,
            'active_page': 'search',
            'searchterm': searchterm,
        })
        return HttpResponse(template.render(context))
    return HttpResponse()


def contact(request):
    template = loader.get_template('blog/template.html')
    context = RequestContext(request, {'active_page': 'imprint','index':True})
    return HttpResponse(template.render(context))