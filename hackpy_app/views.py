# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView,ListView,CreateView,UpdateView,DeleteView,DetailView,FormView
from . import models
from django.core.urlresolvers import reverse_lazy,reverse
from . import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import pdb
import urllib
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
import re
from django.contrib import messages


# Create your views here.
class IndexView(ListView):
    """docstring for ."""
    model = models.UserPost
    paginate_by = 30
    template_name = 'hackpy_app/index.html'
    context_object_name='post_list'

class EditPost(UpdateView):
    """docstring for UpdateView."""
    model = models.UserPost
    fields = ("post_title","post_link")

class DeletePost(DeleteView):
    """docstring for DeletePost."""
    model = models.UserPost
    success_url = reverse_lazy('hackpy_app:index')

class EditComment(UpdateView):
    """docstring for UpdateView."""
    model = models.PostComment
    fields = ("comment_text",)

class DeleteComment(DeleteView):
    """docstring for DeletePost."""
    model = models.PostComment
    def get_success_url(self):
        post = self.object.post
        return reverse_lazy('hackpy_app:post_detail',kwargs={'id': post.id})

class CreateUser(CreateView):
    """docstring for CreateStudent."""
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("hackpy_app:index")
    template_name = "hackpy_app/signup.html"

    def form_valid(self, form):
        # username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        # new_user = authenticate(self.request,username=username, password=password)
        new_user = form.save()
        login(self.request, new_user,backend='django.contrib.auth.backends.ModelBackend')
        return super(CreateUser, self).form_valid(form)

class PostCreate(LoginRequiredMixin,CreateView):
    """docstring for ."""
    form_class = forms.UserPostForm
    template_name = 'hackpy_app/post.html'
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.post_host = form.cleaned_data['post_link'].split("//")[-1].split("/")[0].split('?')[0]
        self.object.save()
        return super(PostCreate,self).form_valid(form)

class UserLogin(LoginView):
    """docstring for UserLogin."""
    form_class = forms.UserLoginForm
    template_name = 'hackpy_app/login.html'


@method_decorator(login_required, name = 'post')
class PostDetail(CreateView,DetailView):
    """docstring for PostDetail."""
    model = models.UserPost
    template_name = 'hackpy_app/post_detail.html'
    context_object_name='post_detail'
    form_class = forms.UserCommentForm

    def get_object(self):
        object = super(PostDetail,self).get_object()
        object.last_accessed = timezone.now()
        object.save()
        return object

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = forms.UserCommentForm
        context['comments'] = models.PostComment.objects.filter(userpost= self.kwargs['pk'])
        print(context['comments'])
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.userpost = models.UserPost.objects.get(pk=self.kwargs['pk'])
        self.object.user = self.request.user
        parent_obj = None
        try:
            self.object.parent_id = int(self.request.POST.get("parent_id"))
        except Exception as e:
            self.object.parent = None
        if self.object.parent:
            parent_qs = models.PostComment.objects.filter(id=self.object.parent_id)
            if parent_qs.exists():
                parent_obj = parent_qs.first()
                self.object.parent = parent_obj
        self.object.save()
        form.save()
        return super(PostDetail, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('hackpy_app:post_detail',args=(self.kwargs['pk'],))

@login_required
def upvote(request):
    if request.method == "POST":
        try:
            vote = models.PostVote()
            vote.user = request.user
            post_id = request.POST.get('post_id')
            vote.userpost = models.UserPost.objects.get(pk=post_id)
            vote.save()
            return HttpResponseRedirect(reverse('hackpy_app:index'))
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse('hackpy_app:index'))
    return HttpResponseRedirect(reverse('hackpy_app:index'))

def search(request):
    q = request.GET['q']
    vector = SearchVector('post_title')
    query = SearchQuery(q)
    # post_list = models.UserPost.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
    post_list = models.UserPost.objects.filter(post_title__search=q)
    context={
    'post_list' : post_list
    }
    return render(request,'hackpy_app/index.html',context)

def from_site(request,post_host):
    post_list = models.UserPost.objects.filter(post_host=post_host)
    context={
    'post_list' : post_list
    }
    return render(request,'hackpy_app/index.html',context)
#for crawling hackernews homepage
def get_comment(post,user):
    request_data = urllib.urlopen("https://news.ycombinator.com/item?id="+post.post_link_id)
    soup     = BeautifulSoup(request_data, 'html.parser')
    all_comment = soup.find_all("div", class_="comment")
    for com in all_comment:
        post.comments.create(comment_text=com.text,user=user)

def crawl_task():
    request_data = urllib.urlopen("https://news.ycombinator.com/")
    soup     = BeautifulSoup(request_data, 'html.parser')
    all_post = soup.find_all("a", class_="storylink")
    all_id   = soup.find_all("span", class_="age")
    all_host = soup.find_all("span", class_="sitestr")
    user     = User.objects.get(id="1")
    for post,post_id,host in zip(all_post,all_id,all_host):
        extract_id = re.findall('\d+', post_id.next_element.get('href'))[0]
        extract_host = host.text
        if models.UserPost.objects.filter(post_link_id=extract_id).first() is None:
            post = models.UserPost.objects.create(user_id=user.id,post_link=post.get('href'),post_title=post.text,post_link_id=extract_id,post_host=extract_host)
            get_comment(post,user)
