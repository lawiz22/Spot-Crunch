# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-31 19:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spotify_app', '0003_auto_20190331_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='isrc',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
