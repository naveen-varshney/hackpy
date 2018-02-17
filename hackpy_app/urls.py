from django.conf.urls import url,include
from django.contrib import admin
from .views import IndexView,CreateUser,PostCreate,UserLogin,PostDetail,EditPost,DeletePost,upvote
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
app_name = 'hackpy_app'
urlpatterns = [
url(r'^$',IndexView.as_view(),name='index'),
url(r'^login/$', UserLogin.as_view(redirect_authenticated_user=True), name='login'),
url(r'^logout/$', auth_views.logout, name='logout'),
url(r'^signup/$', CreateUser.as_view(), name='signup'),
url(r'^create/$', PostCreate.as_view(), name='post'),
url(r'^post_detail/(?P<pk>[0-9]+)/$', PostDetail.as_view(), name='post_detail'),
url(r'^post_update/(?P<pk>[0-9]+)/$', EditPost.as_view(), name='post_update'),
url(r'^post_delete/(?P<pk>[0-9]+)/$', DeletePost.as_view(), name='post_delete'),
url(r'^vote/$', upvote, name='vote'),
]
