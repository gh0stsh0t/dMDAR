from django.shortcuts import render, redirect
from django.db.models import Count, Avg
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from datetime import datetime
from operator import itemgetter

# functions here

def getMovieIdsFromSpecial(movie_special):
    return list(Movie.objects.filter(special=movie_special).values_list("id", flat=True))

# Create your views here.


def index(request):
    context = {}
    all_movies = Movie.objects.all()
    context['featured'] = Movie.objects.filter(special=Movie.FEATURED)
    context['trending'] = Movie.objects.filter(special=Movie.TRENDING)
    new_released_movies = all_movies.order_by('-time_posted')[:5]

    # trending movie ratings
    trending_movie_ratings = []
    for movie_id in getMovieIdsFromSpecial(Movie.TRENDING):
        trending_movie_ratings.append(list(Review.objects.select_related('movie').values_list('rating', flat=True).filter(movie=int(movie_id))))
    trending_avg_rating_list = []
    for lst in trending_movie_ratings:
        trending_avg_rating_list.append(sum(lst) / float(len(lst)))
    context['trending_movie_list'] = list(zip(context['trending'], trending_avg_rating_list))

    # featured movie ratings
    featured_movie_ratings = []
    for movie_id in getMovieIdsFromSpecial(Movie.FEATURED):
        featured_movie_ratings.append(list(Review.objects.select_related('movie').values_list('rating', flat=True).filter(movie=int(movie_id))))
    featured_avg_rating_list = []
    for lst in featured_movie_ratings:
        featured_avg_rating_list.append(sum(lst) / float(len(lst)))

    context['featured_movie_list'] = list(zip(context['featured'], featured_avg_rating_list))

    # new released movie ratings
    new_released_movie_ratings = []
    for movie in new_released_movies:
        new_released_movie_ratings.append(list(Review.objects.select_related('movie').values_list('rating', flat=True).filter(movie=int(movie.id))))
    new_released_avg_rating_list = []
    for lst in new_released_movie_ratings:
        new_released_avg_rating_list.append(sum(lst) / float(len(lst)))

    context['new_released_movie_list'] = list(zip(new_released_movies, new_released_avg_rating_list))

    # highest rated movie ratings
    highest_rated_movie_ratings = []
    for movie in all_movies:
        highest_rated_movie_ratings.append(list(Review.objects.select_related('movie').values_list('rating', flat=True).filter(movie=int(movie.id))))
    highest_rated_avg_ratings_list = []
    for lst in highest_rated_avg_ratings_list:
        highest_rated_avg_ratings_list.append(sum(list) / float(len(lst)))
    
    context['highest_rated_movie_list'] = sorted(list(zip(all_movies, highest_rated_avg_ratings_list)), key=itemgetter(1), reverse=True)

    return render(request, 'home.html', context)


def catalog(request, page=0):
    context = {}
    offset = page * 10
    m = Movie.objects.annotate(Count('Review'), Avg('Review__rating'))
    if request.method == 'GET':
        sorter = request.GET.get('sort', '')
        order = request.GET.get('order', '-')
        search = request.GET.get('search', '')
        if sorter == 'az':
            sorter = 'title'
        elif sorter == 'release':
            sorter = 'release_date'
        elif sorter == 'score':
            sorter = 'Review__rating__ave'
        elif sorter == 'reviews':
            sorter = 'Review__count'
        else:
            sorter = 'time_posted'
        context['movies'] = m.filter(title__contains=search).order_by(order+sorter)[0 + offset:10 + offset]

    else:
        context['movies'] = m.all().order_by('-time_posted')[0 + offset:10 + offset]
    return render(request, 'catalog.html', context)


def details(request, movie_id):
    context = {}
    context['movie'] = Movie.objects.get(id=movie_id)
    return render(request, 'details.html', context)


def user(request, username):
    context = {}
    context['user'] = User.objects.get(username=username)
    if username == request.session['user']:
        context['editable'] = True
    else:
        context['editable'] = False
    return render(request, 'user.html', context)


def login(request):
    context = {}
    if request.method == 'POST':
        m = User.objects.get(adminuser=request.POST['username'])
        if m.password == request.POST['password']:
            request.session['id'] = m.id
            request.session['user'] = m.username
            request.session['type'] = m.usertype
            return redirect('/')
        else:
            context['fail'] = True
            return render(request, 'signin.html', context)
    else:
        return redirect('/')


def logout(request):
    try:
        del request.session['id']
        del request.session['user']
        del request.session['type']
    except KeyError:
        pass
    return redirect('/')


def review(request):
    pass


def post(request):
    pass
