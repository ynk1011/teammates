from django import forms
from django.forms import fields
from .models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'body', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author_name', 'comment_text')
