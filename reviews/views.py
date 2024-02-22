from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from movies.models import Movie

def review_list(request, movie_id):
    reviews = Review.objects.filter(movie_id=movie_id)
    return render(request, 'reviews/review_list.html', {'reviews': reviews, 'movie_id': movie_id})

def submit_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user  # Assumes you are using Django's built-in User model for authentication
            review.save()
            return redirect('review_list', movie_id=movie_id)
    else:
        form = ReviewForm()

    return render(request, 'reviews/submit_review.html', {'form': form, 'movie': movie})