from django.shortcuts import render, redirect
from django.db.models import Count, Avg
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from datetime import datetime
from operator import itemgetter
from django.db.models import Avg, Func

# functions here


# Create your views here.


def index(request):
    context = {}

    # sending context if user is logged in or not
    context['user_logged'] = False
    try:
        context['username'] = request.session['user']
        context['user_pic'] = User.objects.get(username=context['username']).display_pic
        context['user_logged'] = True
    except:
        pass

    m = Movie.objects.annotate(Avg('review__rating'))
    context['featured'] = m.filter(special=Movie.FEATURED)[:7]
    context['trending'] = m.filter(special=Movie.TRENDING)[:7]
    context['new_release'] = m.all().order_by('-release_date')[:7]
    context['highest_rated'] = m.order_by('-review__rating__avg')[:7]

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
        try:
            m = User.objects.get(username=request.POST['username'])
            if m.password == request.POST['password']:
                request.session['id'] = m.id
                request.session['user'] = m.username
                request.session['type'] = m.usertype
                return redirect('/')
            else:
                context['fail'] = True
                return render(request, 'home.html', context)
        except:
            context['fail'] = True
            return render(request, 'home.html', context)
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

def signup(request):
    context = {}
    return render(request, 'signup.html', context)


def review(request):
    pass


def post(request):
    pass
