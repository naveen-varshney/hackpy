# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-21 14:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackpy_app', '0017_auto_20180221_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpost',
            name='post_host',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='post_title',
            field=models.CharField(max_length=400),
        ),
    ]
