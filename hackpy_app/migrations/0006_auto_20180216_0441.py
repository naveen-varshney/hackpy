# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-16 04:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackpy_app', '0005_auto_20180216_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to='hackpy_app.User'),
        ),
    ]
