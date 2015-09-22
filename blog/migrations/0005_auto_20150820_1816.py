# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150716_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='reality_image',
            field=models.ImageField(upload_to=b'reality/%Y/', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='story_image',
            field=models.ImageField(upload_to=b'story/%Y/', blank=True),
        ),
    ]
