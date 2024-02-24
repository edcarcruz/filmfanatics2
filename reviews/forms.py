from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class EditReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']