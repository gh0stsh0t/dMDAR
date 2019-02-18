from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('movie/<int:movie_id>', views.details, name='details'),
    path('user/<string:username>', views.user, name='user'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]