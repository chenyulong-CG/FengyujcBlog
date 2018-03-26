from django import forms
from .models import Comment, Email


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ['name', 'email', 'title', 'text']
