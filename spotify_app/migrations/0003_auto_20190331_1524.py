# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-31 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_app', '0002_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='upc',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='isrc',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='track',
            name='songkey',
            field=models.FloatField(null=True),
        ),
    ]
