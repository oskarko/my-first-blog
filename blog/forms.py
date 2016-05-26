from django import forms
from .models import Post
from .models import Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        # con widgets colocaremos asteriscos como entrada del password
        widgets = {
            'password': forms.PasswordInput(),
        }
