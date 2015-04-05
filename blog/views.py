from django.shortcuts import render
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from django.http import HttpResponse
from blog.models import Post

def index(request):
    post_list = Post.objects.order_by('-pub_date')[:5]
    template = loader.get_template('blog/template.html')
    context = RequestContext(request, {
        'post_list': post_list,
	'index' : True,
    })
    return HttpResponse(template.render(context))

def get_next_post(request, id):
    # -1 offset, because ids are 1-indexed in rendered HTML file
    id = max(int(id) - 1, 0)
    post_list = Post.objects.order_by('pub_date')[int(id):int(id)+1]
    html = render_to_string('blog/template.html', {'post_list': post_list,})
    return HttpResponse(html)
