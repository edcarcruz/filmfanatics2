from django.urls import path
from .views import review_list, submit_review

urlpatterns = [
    path('movies/<int:movie_id>/reviews/', review_list, name='review_list'),
    path('movies/<int:movie_id>/submit_review/', submit_review, name='submit_review'),
]