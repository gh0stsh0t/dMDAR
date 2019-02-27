from django.forms import ModelForm
from .models import User, Movie, Review


class UserModelForm(ModelForm):
    class Meta:
        model = User
        exclude = ['id']


class MovieModelForm(ModelForm):
    class Meta:
        model = Movie
        exclude = ['id', 'isactive', 'special', 'time_posted', 'posted_by']


class ReviewModelForm(ModelForm):
    class Meta:
        model = Review
        exclude = ['id', 'reviewer', 'movie', 'time_posted']
