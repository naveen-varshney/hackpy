from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms
from . import models


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder': 'Password again'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    class Meta:
        fields = ("username","password1","password2")
        model = User

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = "Display name"
        self.fields["password1"].label = "Password"
        self.fields["password2"].label = "Password confirmation"


class UserPostForm(forms.ModelForm):
    """docstring for UserPostForm."""
    class Meta:
        """docstring for Meta."""
        model = models.UserPost
        fields = ('post_title','post_link')
        widgets ={
        'post_title': forms.TextInput(attrs={'class':'form-control'}),
        'post_link': forms.TextInput(attrs={'class':'form-control'}),
        }
class UserLoginForm(AuthenticationForm):
    """docstring for UserLoginForm."""
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    class Meta:
        model = User

class UserCommentForm(forms.ModelForm):
    """docstring for UserCommentForm."""
    class Meta:
        model = models.PostComment
        fields = ('comment_text',)
        widgets ={
        'comment_text': forms.Textarea(attrs={'class':'form-control','rows' : '5','col' :'10','placeholder': 'Write a comment here..'}),
        }
