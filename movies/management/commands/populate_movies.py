import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from movies.models import Movie
import random

class Command(BaseCommand):
    help = 'Populate the movies list with data from random pages of an external API'

    def handle(self, *args, **options):
        # Clear existing movies
        Movie.objects.all().delete()

        # Fetch random page number
        total_pages = 1000  # Set a reasonable maximum page number
        random_page = random.randint(1, total_pages)

        # Fetch movie data from the API (replace with your API logic)
        api_url = 'https://api.themoviedb.org/3/discover/movie'
        api_key = '64072b1e511fe9ad82ab3a4c9d4cc88e'
        params = {'api_key': api_key, 'sort_by': 'popularity.desc', 'page': random_page}
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            movies_data = response.json().get('results', [])
            
            # Create Movie objects from API data
            for movie_data in movies_data:
                Movie.objects.create(
                    title=movie_data['title'],
                    release_date=movie_data['release_date'],
                    genre=','.join(movie_data.get('genres', [])),
                    # Add other fields as needed
                )

            self.stdout.write(self.style.SUCCESS('Movies successfully populated'))
        else:
            self.stderr.write(self.style.ERROR(f'Failed to fetch movies from API: {response.status_code}'))