# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-01 02:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_app', '0007_auto_20190331_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='like_it',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
