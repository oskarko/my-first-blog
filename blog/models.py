from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)  # campo obligatorio
    text = MarkdownxField()  # campo obligatorio
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)  # campo NO obligatorio

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


# clases objeto para guardar posteriormente en BD -> modelos!
class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)  # por defecto vale FALSE

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Document(models.Model):
    author = models.ForeignKey('auth.User', default=1)
    docfile = models.FileField(upload_to='documents/%Y')


class Profil(models.Model):
    user = models.OneToOneField(User, related_name='profil')  # 1 to 1 link with Django User
    password2 = models.CharField(max_length=40, blank=True, null=True)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
