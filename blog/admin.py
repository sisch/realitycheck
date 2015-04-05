from django.contrib import admin
from blog.models import Post
import time
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
  list_display = ('title','pub_date', 'get_pub_date_unix')
  fields = (('title','pub_date'),('reality','story'))
  def get_pub_date_unix(self, instance):
    return "<a href='http://realitycheck.plant.canopus.uberspace.de/#{}'>Link</a>".format(int(time.mktime(instance.pub_date.timetuple())))
  get_pub_date_unix.allow_tags = True
  pass

admin.site.register(Post,BlogAdmin)
