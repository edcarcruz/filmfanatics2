from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm, EditReviewForm
from movies.models import Movie
from django.http import HttpResponseBadRequest
from movies.utils.api import fetch_movie_data
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import json

@login_required
def review_list(request, movie_id):
    # Fetch movie data from the API
    movie_data = fetch_movie_data(movie_id)

    if not movie_data or 'title' not in movie_data:
        return render(request, 'reviews/review_list.html', {'error': 'Movie not found'})

    # Ensure movie title is extracted from the dictionary
    movie_title = movie_data['title']

    # Fetch reviews for the current movie title
    reviews = Review.objects.filter(movie_details__iexact=movie_title)

    return render(request, 'reviews/review_list.html', {'reviews': reviews, 'movie_data': movie_data})

@login_required
def add_review(request, movie_id):
    # Fetch movie data from the API
    movie_data = fetch_movie_data(movie_id)

    if not movie_data:
        # Handle the case where movie data couldn't be fetched
        return render(request, 'reviews/add_review.html', {'error': 'Movie not found'})

    existing_review = Review.objects.filter(user=request.user.userprofile, movie_details=movie_data.get('title', 'N/A')).first()

    if existing_review:
        # Update existing review
        form = ReviewForm(request.POST, instance=existing_review)
    else:
        # Process the review form submission
        form = ReviewForm(request.POST)

    if form.is_valid():
        review = form.save(commit=False)
        review.user = request.user.userprofile
        review.movie_details = movie_data.get('title', 'N/A')
        review.save()
        return redirect('movies:movie_detail', movie_id=movie_id)

    return render(request, 'reviews/add_review.html', {'form': form, 'movie_data': movie_data})


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user.userprofile)

    if request.method == 'POST':
        form = EditReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()

            # Fetch movie data based on review.movie_details (integer or title)
            movie_data = fetch_movie_data(review.movie_details)

            if movie_data:
                # Use reverse to generate the correct redirect URL
                redirect_url = reverse('movies:movie_detail', args=[movie_data.get('id', 0)])  # Use args for single argument
                return redirect(redirect_url)
            else:
                # Handle case where movie data not found
                return render(request, 'reviews/edit_review.html', {'error': 'Movie not found'})
    else:
        form = EditReviewForm(instance=review)

    return render(request, 'reviews/edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user.userprofile)

    if request.method == 'POST':
        # Assuming you have a ForeignKey field named 'movie_details' in the Review model
        movie_details = review.movie_details
        # Fetch the movie based on the movie_details
        movie_data = fetch_movie_data(movie_details)

        review.delete()

        if movie_data:
            # Use reverse to generate the correct redirect URL
            redirect_url = reverse('movies:movie_detail', args=[movie_data.get('id', 0)])  # Use args for single argument
            return redirect(redirect_url)
        else:
            # Handle case where movie data not found
            return render(request, 'reviews/delete_review.html', {'error': 'Movie not found'})

    return render(request, 'reviews/delete_review.html', {'review': review})