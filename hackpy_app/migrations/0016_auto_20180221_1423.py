# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-21 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackpy_app', '0015_auto_20180218_1330'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpost',
            name='post_link_host',
            field=models.CharField(default='fuck', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userpost',
            name='post_link_id',
            field=models.CharField(default='fuck', max_length=100),
            preserve_default=False,
        ),
    ]
