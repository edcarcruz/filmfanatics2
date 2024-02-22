from django.urls import path
from .views import register, profile

urlpatterns = [
    # Other URL patterns
    path('register/', register, name='register'),
    path('accounts/profile/', profile, name='profile'),
]