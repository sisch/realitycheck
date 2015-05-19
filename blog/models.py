from django.db import models

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=200)
  reality = models.TextField(max_length=2500)
  story = models.TextField(max_length=2500)
  pub_date = models.DateTimeField('date published')
  hidden = models.BooleanField(default=False)
