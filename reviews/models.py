from django.db import models
from movies.models import Movie
from users.models import UserProfile
import json



class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    movie_details = models.JSONField()

    def __str__(self):
        return f"{self.user.username} - {self.get_movie_title()} - {self.rating}"
    
    
    def get_movie_title(self):
        return self.movie_details.get('title', 'N/A')