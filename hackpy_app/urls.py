from django.conf.urls import url,include
from django.contrib import admin
from .views import IndexView,CreateUser,PostCreate,UserLogin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
app_name = 'hackpy_app'
urlpatterns = [
url(r'^$',IndexView.as_view(),name='index'),
url(r'^login/$', UserLogin.as_view(redirect_authenticated_user=True), name='login'),
url(r'^logout/$', auth_views.logout, name='logout'),
url(r'^signup/$', CreateUser.as_view(), name='signup'),
url(r'^create/$', PostCreate.as_view(), name='post'),
]
