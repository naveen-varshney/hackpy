# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView,DetailView
from . import models
from django.core.urlresolvers import reverse_lazy
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
# Create your views here.
class IndexView(ListView):
    """docstring for ."""
    model = models.UserPost
    paginate_by = 30
    template_name = 'hackpy_app/index.html'
    context_object_name='post_list'
class CreateUser(CreateView):
    """docstring for CreateStudent."""
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("hackpy_app:index")
    template_name = "hackpy_app/signup.html"

    def form_valid(self, form):
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return super(CreateUser, self).form_valid(form)

class PostCreate(LoginRequiredMixin,CreateView):
    """docstring for ."""
    form_class = forms.UserPostForm
    template_name = 'hackpy_app/post.html'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(PostCreate,self).form_valid(form)

class UserLogin(LoginView):
    """docstring for UserLogin."""
    form_class = forms.UserLoginForm
    template_name = 'hackpy_app/login.html'
