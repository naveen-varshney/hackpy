# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-25 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackpy_app', '0019_auto_20180221_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='post_host',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='post_link_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
