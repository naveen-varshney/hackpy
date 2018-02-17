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
    """docstring for UserPost."""
    user = models.ForeignKey('auth.User',related_name="post_user",on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_link = models.URLField()
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.post_title + " By " + self.user.username

    class Meta:
        ordering = ['-created_at']
    def get_absolute_url(self):
        return reverse('hackpy_app:index')

class PostVote(models.Model):
     user = models.ForeignKey('auth.User',related_name="my_votes",on_delete=models.CASCADE)
     userpost = models.ForeignKey(UserPost,related_name="votes",on_delete=models.CASCADE)
     def __str__(self):
         return self.userpost.post_title + " By " + self.user.username
     def get_absolute_url(self):
         return reverse('hackpy_app:index')

class PostComment(models.Model):
    """docstring for PostComment."""
    userpost = models.ForeignKey(UserPost,related_name="comments",on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User',related_name="my_comments",on_delete=models.CASCADE)
    comment_text = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True,related_name='replies')
    timestamp = models.DateTimeField(auto_now=True)
    class Meta:
        ordering=['-timestamp']

    def __str__(self):
        return self.comment_text + " By " + self.user.username

    def get_absolute_url(self):
        return reverse('hackpy_app:post_detail',args=(self.user.id,))

    def children(self):
        return PostComment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
