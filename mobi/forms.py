from django.forms import ModelForm
from .models import User, Movie, Review
from django.forms.widgets import HiddenInput
from django import forms


class UserModelForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id']


class MovieModelForm(ModelForm):
    class Meta:
        model = Movie
        exclude = ['id', 'isactive', 'special', 'time_posted']
        widgets = {'posted_by': forms.HiddenInput()}


class ReviewModelForm(ModelForm):
    class Meta:
        model = Review
        exclude = ['id', 'reviewer', 'movie', 'time_posted']
