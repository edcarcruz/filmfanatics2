import requests
from django.conf import settings



def fetch_movie_data(identifier=None):
    api_key = '64072b1e511fe9ad82ab3a4c9d4cc88e'

    if identifier is not None and str(identifier).isdigit():
        url = f'https://api.themoviedb.org/3/movie/{identifier}?api_key={api_key}'
    elif identifier is not None:
        url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={identifier}'
    else:
        url = f'https://api.themoviedb.org/3/discover/movie?api_key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        if identifier and not str(identifier).isdigit():  # Handle search results
            data = response.json()
            for movie in data.get('results', []):
                if movie['title'].lower() == identifier.lower():
                    return movie
            return None

        return response.json()  # Return data for numeric IDs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie data: {e}")
        return None
    
def fetch_movie_data_by_title(movie_title):
    api_key = '64072b1e511fe9ad82ab3a4c9d4cc88e'  # Replace with your actual API key
    api_url = 'https://api.themoviedb.org/3/search/movie'
    params = {'api_key': api_key, 'query': movie_title}

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad responses (4xx, 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie data: {e}")
        return None