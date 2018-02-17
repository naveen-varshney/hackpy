# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-17 06:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hackpy_app', '0011_auto_20180216_0455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcomment',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='postcomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hackpy_app.PostComment'),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]