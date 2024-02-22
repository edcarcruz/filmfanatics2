from django.urls import path
from .views import movie_list, movie_detail, home

app_name = 'movies'  # Add this line to set the app_name

urlpatterns = [
    path('movies/', movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('home/', home, name='home'),
]