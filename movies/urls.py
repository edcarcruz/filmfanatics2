from django.urls import path
from .views import movie_list, movie_detail, search_results, home

app_name = 'movies'  # Add this line to set the app_name

urlpatterns = [
    path('', home, name='home'),
    path('movies/', movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('search/', search_results, name='search_results'),
]