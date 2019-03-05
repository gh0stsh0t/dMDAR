from django.db import models
from enum import Enum
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class GenreChoice(Enum):
    ACTION = 'Action'
    ADULT = 'Adult'
    ADVENTURE = 'Adventure'
    ANIMATION = 'Animation'
    BIOGRAPHY = 'Biography'
    COMEDY = 'Comedy'
    CRIME = 'Crime'
    DOCUMENTARY = 'Documentary'
    DRAMA = 'Drama'
    FAMILY = 'Family'
    FANTASY = 'Fantasy'
    FILM = 'Film'
    NOIR = 'Noir'
    GAMESHOW = 'Game - Show'
    HISTORY = 'History'
    HORROR = 'Horror'
    MUSICAL = 'Musical'
    MUSIC = 'Music'
    MYSTERY = 'Mystery'
    NEWS = 'News'
    REALITY = 'Reality - TV'
    ROMANCE = 'Romance'
    SCIFI = 'Sci - Fi'
    SHORT = 'Short'
    SPORT = 'Sport'
    TALKSHOW = 'Talk - Show'
    THRILLER = 'Thriller'
    WAR = 'War'
    WESTERN = 'Western'


class SiteChoice(Enum):
    AMAZON = 'Amazon'
    GOOGLE = 'Google Play'
    ITUNES = 'iTunes'
    NETFLIX = 'Netflix'


class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    ADMIN, USER = True, False
    usertypes = ((USER, 'User'), (ADMIN, 'Admin'))
    usertype = models.BooleanField(choices=usertypes, default=usertypes[0][0])
    display_pic = models.ImageField(null=True, upload_to='display_pic/')
    description = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.username


class Genre(models.Model):
    genre = models.CharField(choices=[(tag.value, tag.name) for tag in GenreChoice], max_length=15, primary_key=True)

    def __str__(self):
        return self.genre


class Actor(models.Model):
    firstname = models.CharField(max_length=35)
    lastname = models.CharField(max_length=35)
    link = models.URLField(null=True)
    picture = models.ImageField(null=True, upload_to='artist_pic/')

    def __str__(self):
        return "{}, {}".format(self.lastname, self.firstname)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    isactive = models.BooleanField(default=True)
    duration = models.IntegerField(validators=[MinValueValidator(0)], null=True)
    synopsis = models.TextField(null=True)
    G, PG, PG13, R, X = 'G', 'PG', 'PG-13', 'R', 'X'
    restrictions = ((X, 'General Audience'), (PG, 'Parental Guidance Suggested'), (PG13, 'Parents Strongly Cautioned'),
                    (R, 'Restricted '), (X, 'X-Rated'))
    restriction = models.CharField(choices=restrictions, max_length=5)
    release_date = models.DateField(null=True)
    # special is used for trending and featured movies
    TRENDING = 1
    FEATURED = 2
    NORMAL = 0
    specials = ((NORMAL, 'Normal'), (TRENDING, 'Trending'), (FEATURED, 'Featured'))
    special = models.IntegerField(choices=specials, default=specials[0][0])
    trailer = models.URLField(null=True)
    director = models.CharField(max_length=75, null=True)
    background = models.ImageField(upload_to='bg/')
    poster = models.ImageField(upload_to='poster/')
    time_posted = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, blank=True)
    cast = models.ManyToManyField(Actor, through=Cast, blank=True)

    def __str__(self):
        return self.title


class Cast(models.Model):
    role = models.CharField(max_length=35)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    def __str__(self):
        return self.actor.lastname + ", " + self.actor.firstname + " - " + self.rol


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Review by {} for {}".format(self.reviewer.username, self.movie.title)


class Watch(models.Model):
    site = models.CharField(choices=[(tag.value, tag.name) for tag in SiteChoice], max_length=15)
    url = models.URLField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
