# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def exchange_hidden_to_visible(apps, schema_editor):
    Post = apps.get_model("blog", "Post")
    for p in Post.objects.all():
        p.visible = not p.hidden
        p.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.RunPython(exchange_hidden_to_visible),
        migrations.RemoveField(
            model_name='post',
            name='hidden',
        ),
        
    ]
