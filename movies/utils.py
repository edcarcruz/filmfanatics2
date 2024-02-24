import requests
from django.conf import settings

def fetch_movie_data(movie_id):
    api_key = '64072b1e511fe9ad82ab3a4c9d4cc88e'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None