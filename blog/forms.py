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


class DocumentForm(forms.Form):

    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


class ContactForm(forms.Form):

    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'name'}), label=(u'name'), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'email'}), label=(u'email'), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Please enter the message'}), required=True)
