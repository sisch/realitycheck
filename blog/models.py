from django.db import models
import re

wordcount = re.compile(r"\w+")

# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length=200)
  reality = models.TextField(max_length=2500)
  story = models.TextField(max_length=2500)
  pub_date = models.DateTimeField('date published')
  hidden = models.BooleanField(default=False)

  @property
  def reality_wordcount(self):
      return len(wordcount.findall(self.reality))
  @property
  def story_wordcount(self):
      return len(wordcount.findall(self.story))
  