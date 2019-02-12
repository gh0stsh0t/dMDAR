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
    display_pic = models.ImageField()

    def __str__(self):
        return self.username


class Movie(models.Model):
    title = models.CharField()
    isactive = models.BooleanField(default=True)
    duration = models.IntegerField(validators=[MinValueValidator(0)])
    synopsis = models.TextField()
    G, PG, PG13, R, X = 'G', 'PG', 'PG-13', 'R', 'X'
    restrictions = ((X, 'General Audience'), (PG, 'Parental Guidance Suggested'), (PG13, 'Parents Strongly Cautioned'),
                    (R, 'Restricted '), (X, 'X-Rated'))
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

    def __str__(self):
        return self.title


class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    time_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Review by {} for {}".format(self.reviewer.username, self.movie.title)


class Genre(models.Model):
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
    genres = ()
    genre = models.CharField(choices=genres)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return self.genre


class Actor(models.Model):
    firstname = models.CharField(max_length=35)
    lastname = models.CharField(max_length=35)
    link = models.URLField()
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return "{}, {}".format(self.lastname, self.firstname)


class Watch(models.Model):
    AMAZON = 'Amazon'
    GOOGLE = 'Google Play'
    ITUNES = 'iTunes'
    NETFLIX = 'Netflix'
    sites = ((AMAZON, 'Amazon'), (GOOGLE, 'Google Play'), (ITUNES, 'iTunes'), (NETFLIX, 'Netflix'))
    site = models.CharField(choices=sites)
    url = models.URLField()
    movie = models.ForeignKey(Movie)
