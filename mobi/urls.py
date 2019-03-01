from django.urls import path
from . import views
app_name = 'mobi'

app_name = 'mobi'
urlpatterns = [
    path('', views.index, name='index'),
    path('catalog', views.catalog, name='catalog'),
    path('movie/<int:movie_id>', views.details, name='details'),
    path('user/<str:username>', views.user, name='user'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name="signup"),
    path('movie/<int:movie_id>/review', views.review, name='review'),
    path('movie', views.post, name='post'),
]