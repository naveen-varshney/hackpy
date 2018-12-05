# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UserPost)
admin.site.register(models.PostComment)
admin.site.register(models.PostVote)
