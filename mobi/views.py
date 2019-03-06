from django.shortcuts import render, redirect, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.forms import formset_factory
from .models import Movie, Review, Genre, Actor, Watch, User, GenreChoice
from .forms import UserModelForm, MovieModelForm, ReviewModelForm, WatchModelForm
from datetime import datetime
from operator import itemgetter
from django.db.models import Avg, Func, Count
from django.core import serializers
from django.forms.models import model_to_dict


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

    return render(request, 'index.html', context)


def catalog(request, page=1):
    context = {}

    # sending context if user is logged in or not
    context['user_logged'] = False
    try:
        context['username'] = request.session['user']
        context['user_pic'] = User.objects.get(username=context['username']).display_pic
        context['user_logged'] = True
    except:
        pass

    context['genres'] = list(GenreChoice)

    offset = page - 1
    m = Movie.objects.annotate(Count('review'), Avg('review__rating'))
    if request.method == 'POST' and request.is_ajax():
        sorter = request.POST.get('sort', '')
        order = request.POST.get('order', '-')
        search = request.POST.get('search', '')
        min_rating = float(request.POST.get('min', 0))
        max_rating = float(request.POST.get('max', 5))
        show = int(request.POST.get('show', 0))
        offset *= show

        genres = []
        # For rendering the list of genres please use the genres context
        # example usage: for genre in GenreChoice:
        #                    <input type="text" name="{{genre.name}}" value="{{genre.value}}"/>
        for genre in GenreChoice:
            try:
                genres.append(request.POST[genre.name])
            except KeyError:
                pass

        if sorter == 'az':
            sorter = 'title'
            order = ''
        elif sorter == 'release':
            sorter = 'release_date'
        elif sorter == 'score':
            sorter = 'review__rating__avg'
        elif sorter == 'reviews':
            sorter = 'review__count'

        wanted_genre = Genre.objects.filter(genre__in=genres).values('genre')
        #sa genres__in to na part
        filters = dict(title__contains=search, review__rating__avg__range=(min_rating, max_rating), genres__genre__in=wanted_genre, isactive=True)
        context['movies'] = m.filter(**filters).order_by(order + sorter)[0 + offset:show + offset]
        print(sorter, order, search, min_rating, max_rating, offset, show)
        # print(context['movies'][0:2].title)
        # return JsonResponse(serializers.serialize('json', context['movies']), safe=False)
        catalog_template = render_to_string('catalog-movies.html', context, request)
        return JsonResponse({'catalog_template':catalog_template}, safe=False)
        # return render(request, 'catalog.html', context)
    else:
        context['movies'] = m.all().order_by('-time_posted')[0 + offset:16 + offset]
    return render(request, 'catalog.html', context)


def details(request, movie_id):
    context = {}
    context['user_logged'] = False

    try:

        context['username'] = request.session['user']

        context['user_pic'] = User.objects.get(username=context['username']).display_pic

        context['user_logged'] = True

    except:

        pass
    context['movie'] = Movie.objects.annotate(Avg('review__rating')).get(id=movie_id)
    reviews = context['movie'].review_set
    context['overall'] = context['movie'].review__rating__avg
    context['count'] = reviews.count()
    context['breakdown'] = [reviews.filter(rating=rating).count() for rating in range(6)]
    context['reviews'] = reviews.all()
    context['cast'] = context['movie'].cast.all()
    context['watch'] = context['movie'].watch_set.all()
    context['trending'] = Movie.objects.annotate(Avg('review__rating')).filter(special=Movie.TRENDING)
    context['top_rev'] = reviews.all().order_by('-rating')
    return render(request, 'details.html', context)


def user(request, username):
    context = {}
    # sending context if user is logged in or not
    context['user_logged'] = False
    try:
        context['username'] = request.session['user']
        context['user_pic'] = User.objects.get(username=context['username']).display_pic
        context['user_logged'] = True
    except:
        pass
    
    if username != context['username']:
        return redirect('/user/'+context['username'])
    else:
        # m = Movie.objects.annotate(Avg('review__rating'))
        # context['user'] = u.get(username=username)
        # context['reviews'] = Review.objects.filter(reviewer=request.session['id'])
        # context['movies'] = m
        user = User.objects.annotate(Count('review', distinct=True), Count('movie', distinct=True))
        context['user'] = user.get(username=username)
        reviews = Review.objects
        min_rating = request.GET.get('min', 0)
        max_rating = request.GET.get('max', 5)
        status = request.GET.get('status_r', 'active') == 'active'
        context['reviews'] = reviews.filter(rating__range=(min_rating, max_rating)).filter(movie__isactive=status).filter(reviewer=context['user'])
        print(context['reviews'])
        movies = Movie.objects.filter(posted_by=context['user'])
        status = request.GET.get('status_m', 'active') == 'active'

        # Hello, code below should be replaced with the ajax function of catalog

        context['genres'] = GenreChoice
        m = movies.annotate(Count('review'), Avg('review__rating'))
        if request.method == 'POST':
            sorter = request.POST.get('sort', '')
            order = request.POST.get('order', '-')
            search = request.POST.get('search', '')
            min_rating = float(request.POST.get('min', 0))
            max_rating = float(request.POST.get('max', 5))
            show = int(request.POST.get('show', 0))

            genres = []
            # For rendering the list of genres please use the genres context
            # example usage: for genre in GenreChoice:
            #                    <input type="text" name="{{genre.name}}" value="{{genre.value}}"/>
            for genre in GenreChoice:
                try:
                    genres += request.POST[genre.name]
                except KeyError:
                    pass
            print(genres)

            if sorter == 'az':
                sorter = 'title'
            elif sorter == 'release':
                sorter = 'release_date'
            elif sorter == 'score':
                sorter = 'review__rating__avg'
            elif sorter == 'reviews':
                sorter = 'review__count'
            else:
                sorter = 'time_posted'

        filters = dict(title__contains=search, review__rating__range=(min_rating, max_rating), genres__in=genres, isactive=status)
        context['movies'] = m.filter(**filters).order_by(order + sorter)[0:show]
    try:
        if username == request.session['user']:
            context['editable'] = True
        else:
            context['editable'] = False
    except:
        pass
    
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
                context['fail'] = False
                return JsonResponse(context)
            else:
                context['fail'] = True
                # return render(request, 'index.html', context)
                return JsonResponse(context)
        except:
            context['fail'] = True
            return JsonResponse(context)
    else:
        context['fail'] = False
        return JsonResponse(context)


def logout(request):
    try:
        del request.session['id']
        del request.session['user']
        del request.session['type']
    except KeyError:
        pass
    return redirect('/')

    return render(request, 'signup.html', context)


def review(request, movie_id):
    # This is placeholder code for ajax review code
    context = {}
    # For checking if logged in, manual user creation huhu
    try:
        user_loggedin = User.objects.get(request.session['id'])
    except KeyError:
        return redirect('/movie/' + str(movie_id))
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = ReviewModelForm(request.POST)
        if form.is_valid():
            review = form.save()
            # Assign foreign keys below
            review.movie = movie
            review.reviewer = user_loggedin
            return redirect('/movie/' + str(movie_id))
        else:
            context['form'] = form
            return render(request, 'review.html', context)
    else:
        context['form'] = ReviewModelForm()
        return render(request, 'review.html', context)


def edit_review(request, movie_id, review_id):
    # This is placeholder code for ajax review code
    context = {}
    context['user_logged'] = False

    try:

        context['username'] = request.session['user']

        context['user_pic'] = User.objects.get(username=context['username']).display_pic

        context['user_logged'] = True

    except:

        pass
    review = Review.objects.get(id=review_id)
    # For checking if logged in, manual user creation huhu
    try:
        User.objects.get(request.session['id'])
    except KeyError:
        return redirect('/movie/' + str(movie_id))
    if request.method == 'POST':
        form = ReviewModelForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            return redirect('/movie/' + str(movie_id))
        else:
            context['form'] = form
            return render(request, 'review_edit.html', context)
    else:
        context['form'] = ReviewModelForm(instance=review)
        return render(request, 'review_edit.html', context)


def post(request):
    context = {}
    context['user_logged'] = False

    try:
        context['username'] = request.session['user']
        context['user_pic'] = User.objects.get(username=context['username']).display_pic
        context['user_logged'] = True
    except:
        pass

    if request.method == 'POST':
        movie = MovieModelForm(request.POST, request.FILES)
        watches = formset_factory(WatchModelForm(request.POST))

        if movie.is_valid():
            movie.cleaned_data['id_posted_by'] = User.objects.get(username=context['username']).id
            saved_movie = movie.save()
            if watches.is_valid():
                for watch in watches:
                    temp = watch.save()
                    temp.movie = saved_movie
            return redirect('/')
        else:
            context['form_movie'] = movie
            context['form_watches'] = watches
            return render(request, 'addmovie.html', context)
    else:
        context['form_movie'] = MovieModelForm(initial={'posted_by': User.objects.get(username=context['username']).id})
        context['form_watches'] = formset_factory(WatchModelForm())
        return render(request, 'addmovie.html', context)


def edit_post(request, movie_id):
    context = {}
    context['user_logged'] = False

    try:
        context['username'] = request.session['user']
        context['user_pic'] = User.objects.get(username=context['username']).display_pic
        context['user_logged'] = True
    except:
        pass

    movie = Movie.objects.get(id=movie_id)
    existing_watch = Watch.objects.filter(movie=movie).values()
    watchesFormset = formset_factory(WatchModelForm)
    context['movie'] = movie

    if request.method == 'POST':
        movie = MovieModelForm(request.POST, request.FILES, instance=movie)
        watches = watchesFormset(request.POST, initial=existing_watch)
        if movie.is_valid():
            saved_movie = movie.save()
            if watches.is_valid():
                for watch in watches:
                    temp = watch.save()
                    temp.movie = saved_movie
            return redirect('/movie/'+str(movie_id))
        else:
            context['form_movie'] = movie
            context['form_watches'] = watches
            return render(request, 'editmovie.html', context)
    else:
        context['form_movie'] = MovieModelForm(instance=movie)
        context['form_watches'] = watchesFormset(initial=existing_watch)
        return render(request, 'editmovie.html', context)


def edit_user(request, username):
    context = {}
    context['user_logged'] = False

    try:

        context['username'] = request.session['user']

        context['user_pic'] = User.objects.get(username=context['username']).display_pic

        context['user_logged'] = True

    except:

        pass
    user = User.objects.get(id=request.session['id'])
    if request.method == 'POST':
        form = UserModelForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            m = User.objects.get(id=request.session['id'])
            request.session['user'] = m.username
            request.session['type'] = m.usertype

            return redirect('/user/'+m.username)
        else:
            context['form'] = form
            return render(request, 'editprofile.html', context)
    else:
        context['form'] = UserModelForm(instance=user)
        return render(request, 'editprofile.html', context)


def signup(request):
    context = {}

    if request.method == 'POST':
        form = UserModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            print(form.errors)
            return render(request, 'signup.html', context)
    else:
        context['form'] = UserModelForm()
        return render(request, 'signup.html', context)

def submit_movie_search_from_ajax(request):
    movies = []  # Assume no results.
    search_text = ""  # Assume no search
    if request.method == "GET":
        search_text = request.GET.get("movie_search_text", "").strip().lower()
        if len(search_text) < 2:
            search_text = ""
    movie_results = []
    if search_text != "":
        movie_results = Movie.objects.filter(title__icontains=search_text)
    context = {
        "search_text": search_text,
        "movie_search_results": movie_results,
    }

    return render_to_response("search/movie_search_results.html",
                              context)