from django.urls import path
from .views import review_list, add_review, edit_review, delete_review

app_name = 'reviews'

urlpatterns = [
    path('add/<int:movie_id>/', add_review, name='add_review'),
    path('movies/<int:movie_id>/reviews/', review_list, name='review_list'),
    path('edit/<int:review_id>/', edit_review, name='edit_review'),
    path('delete/<int:review_id>/', delete_review, name='delete_review'),
]