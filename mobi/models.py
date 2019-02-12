from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    ADMIN, USER = True, False
    usertypes = ((ADMIN, 'Admin'), (USER, 'User'))
    usertype = models.BooleanField(choices=usertypes)


class Movie(models.Model):
    title = models.CharField()
    isactive = models.BooleanField(default=True)
    duration = models.IntegerField(validators=[MinValueValidator(0)])
    G, PG, PG13, R, X = 'G', 'PG', 'PG-13', 'R', 'X'
    restrictions = ((X, 'General Audience'), (PG, 'Parental Guidance Suggested'), (PG13, 'Parents Strongly Cautioned'), (R, 'Restricted '), (X, 'X-Rated'))
    restriction = models.CharField(choices=restrictions)
    release_date = models.DateField()
    # special is used for trending and featured movies
    TRENDING = 1
    FEATURED = 2
    NORMAL = 0
    specials = ((TRENDING, 'Trending'), (FEATURED, 'Featured'), (NORMAL, 'Normal'))
    special = models.IntegerField(choices=specials)
    trailer = models.URLField()
    director = models.CharField()
    background = models.ImageField()
    poster = models.ImageField()
    time_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Review(models.Model):
   reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
   movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
   comment = models.TextField()
   rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
   time_posted = models.DateTimeField(auto_now_add=True)


class Genre(models.Model):
    Action
    Adult
    Adventure
    Animation
    Biography
    Comedy
    Crime
    Documentary
    Drama
    Family
    Fantasy
    Film
    Noir
    Game - Show
    History
    Horror
    Musical
    Music
    Mystery
    News
    Reality - TV
    Romance
    Sci - Fi
    Short
    Sport
    Talk - Show
    Thriller
    War
    Western


class GenreLine(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


class Actor(models.Model):
    pass


class ActorLine(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


