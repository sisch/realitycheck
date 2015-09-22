from django.db import models
import re

wordcount = re.compile(r"\w+")

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=200)
  reality = models.TextField(max_length=2500)
  reality_image = models.ImageField(upload_to="reality/%Y/", blank=True)
  story = models.TextField(max_length=2500)
  story_image = models.ImageField(upload_to="story/%Y/", blank=True)
  pub_date = models.DateTimeField('date published')
  visible = models.BooleanField(default=True)
  

  @property
  def reality_wordcount(self):
      return len(wordcount.findall(self.reality))
  @property
  def story_wordcount(self):
      return len(wordcount.findall(self.story))
  
