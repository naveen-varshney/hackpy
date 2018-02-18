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
    fields = ("post_title","post_link")

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
        self.object.save()
        form.save()
        return super(PostDetail, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('hackpy_app:post_detail',args=(self.kwargs['pk'],))

@login_required
def upvote(request):
    if request.method == "POST":
        vote = models.PostVote()
        vote.user = request.user
        post_id = request.POST.get('post_id', '')
        print(post_id)
        vote.userpost = models.UserPost.objects.get(pk=post_id)
        vote.save()
        return HttpResponseRedirect(reverse('hackpy_app:index'))
    return HttpResponseRedirect(reverse('hackpy_app:index'))

def search(request):
    q = request.GET['q']
    vector = SearchVector('post_title')
    query = SearchQuery(q)
    obj_list = models.UserPost.objects.annotate(rank=SearchRank(vector, query)).order_by('-rank')
    context={
    'obj_list' : obj_list
    }
    return render(request,'hackpy_app/search.html',context)
