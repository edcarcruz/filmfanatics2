import requests
from django.conf import settings

def fetch_movie_data(movie_id):
    api_key = settings.MOVIE_API_KEY
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None