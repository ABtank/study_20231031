from django import forms
from django.core.validators import MinLengthValidator

from django.forms import ModelForm, Textarea, CheckboxSelectMultiple, Select, SelectMultiple, CharField
from .models import MyArticle


class MyArticleForm(ModelForm):
    class Meta:
        model = MyArticle
        fields = ['title', 'anouncement', 'text', 'tags']
        widgets = {
            'anouncement': Textarea(attrs={'cols': 80, 'rows': 2}),
            'text': Textarea(attrs={'cols': 80, 'rows': 5}),
            'tags': SelectMultiple(),
        }
