# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-16 04:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hackpy_app', '0006_auto_20180216_0441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postcomment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='postcomment',
            name='userpost',
        ),
        migrations.DeleteModel(
            name='PostComment',
        ),
    ]