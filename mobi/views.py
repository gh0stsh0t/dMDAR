from django.shortcuts import render, redirect
from django.db.models import Count, Avg
from django.http import HttpResponse, HttpResponseRedirect
from .models import Movie, Review, Genre, Actor, Watch, User
from .forms import UserModelForm, MovieModelForm, ReviewModelForm
from datetime import datetime

# Create your views here.


def index(request):
    context = {}
    context['featured'] = Movie.objects.get(special=Movie.FEATURED)
    context['trending'] = Movie.objects.filter(special=Movie.TRENDING)
    context['new_release'] = Movie.objects.all().order_by('-time_posted')[:5]
    return render(request, 'index.html', context)


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


def review(request, movie_id):
    # This is placeholder code for ajax review code
    context = {}
    # For checking if logged in, manual user creation huhu
    try:
        user_loggedin = User.objects.get(request.session['id'])
    except KeyError:
        return redirect('/movie/'+str(movie_id))
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = ReviewModelForm(request.POST)
        if form.is_valid():
            review = form.save()
            # Assign foreign keys below
            review.movie = movie
            review.reviewer = user_loggedin
            return redirect('/movie/'+str(movie_id))
        else:
            context['form'] = form
            return render(request, 'review.html', context)
    else:
        context['form'] = ReviewModelForm()
        return render(request, 'review.html', context)


def edit_review(request, movie_id, review_id):
    # This is placeholder code for ajax review code
    context = {}
    review = Review.objects.get(id=review_id)
    # For checking if logged in, manual user creation huhu
    try:
        User.objects.get(request.session['id'])
    except KeyError:
        return redirect('/movie/'+str(movie_id))
    if request.method == 'POST':
        form = ReviewModelForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            return redirect('/movie/'+str(movie_id))
        else:
            context['form'] = form
            return render(request, 'review_edit.html', context)
    else:
        context['form'] = ReviewModelForm(instance=review)
        return render(request, 'review_edit.html', context)


def post(request):
    context = {}
    if request.method == 'POST':
        form = MovieModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'addmovie.html', context)
    else:
        context['form'] = MovieModelForm()
        return render(request, 'addmovie.html', context)


def edit_post(request, movie_id):
    context = {}
    movie = Movie.objects.get(id=movie_id)
    context['movie'] = movie
    if request.method == 'POST':
        form = MovieModelForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('/movie/'+str(movie_id))
        else:
            context['form'] = form
            return render(request, 'editmovie.html', context)
    else:
        context['form'] = MovieModelForm(instance=movie)
        return render(request, 'editmovie.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'signup.html', context)
    else:
        context['form'] = UserModelForm()
        return render(request, 'signup.html', context)
