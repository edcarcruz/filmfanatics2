from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.http import HttpResponse
from .utils.api import fetch_movie_data, fetch_movie_data_by_title
from django.conf import settings
import requests
from reviews.models import Review
from reviews.forms import ReviewForm


def movie_list(request):
    # Fetch a list of movies from the API
    movies_data = fetch_movie_data()

    if not movies_data:
        # Handle the case where movie data couldn't be fetched
        return render(request, 'movies/movie_list.html', {'error': 'Movies not found'})

    movies = movies_data.get('results', [])  # Adjust this based on the structure of your API response

    return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_detail(request, movie_id=None, movie_title=None):
    if movie_id:
        movie_data = fetch_movie_data(movie_id)
    elif movie_title:
        # Fetch movie data based on the title
        movie_data = fetch_movie_data_by_title(movie_title)
    else:
        return render(request, 'movies/movie_detail.html', {'error': 'Movie not found'})

    if movie_data:
        # Fetch reviews for the current movie title
        reviews = Review.objects.filter(movie_details=movie_data.get('title', 'N/A'))

        context = {
            'movie_data': movie_data,
            'reviews': reviews,
            'review_form': ReviewForm(),  # Include an instance of the review form for submitting new reviews
        }

        return render(request, 'movies/movie_detail.html', context)
    else:
        return render(request, 'movies/movie_detail.html', {'error': 'Movie not found'})

def home(request):
    # Your view logic here
    return render(request, 'movies/home.html')  # Adjust the template name as needed

def search_results(request):
    query = request.GET.get('query')

    if query:
        api_key = '64072b1e511fe9ad82ab3a4c9d4cc88e'
        api_url = 'https://api.themoviedb.org/3/search/movie'
        params = {'api_key': api_key, 'query': query}
        
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            movies_data = response.json().get('results', [])
            context = {'movies_data': movies_data, 'query': query}
            return render(request, 'movies/search_results.html', context)
        else:
            error_message = f'Failed to fetch search results from API: {response.status_code}'
            context = {'error_message': error_message}
            return render(request, 'movies/search_results.html', context)

    else:
        return render(request, 'movies/search_results.html', {'query': query})