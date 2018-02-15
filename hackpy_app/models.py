# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User,PermissionsMixin
from django.core.urlresolvers import reverse
from django.contrib import auth

# Create your models here.

class User(User):
    def __str__(self):
        return "@{}".format(self.username)

class UserPost(models.Model):
    """docstring for ."""
    user = models.ForeignKey('auth.User',related_name="userpost",on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_link = models.URLField()
    created_at = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    def __str__(self):
        return self.post_title + " By " + self.user.username

    class Meta:
        ordering = ['-id']
    def get_absolute_url(self):
        return reverse('hackpy_app:index')
