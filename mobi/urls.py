from django.urls import path
from . import views

app_name = 'mobi'
urlpatterns = [
    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('movie/<int:movie_id>', views.details, name='details'),
    path('user/<str:username>', views.user, name='user'),
    path('user/<str:username>/update', views.edit_user, name='edit_user'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name="signup"),
    path('movie/<int:movie_id>/review', views.review, name='review'),
    path('movie', views.post, name='post'),
    path('movie/<int:movie_id>/update', views.edit_post, name='edit_post'),
    path('search', views.submit_movie_search_from_ajax, name='movie_list'),
]
