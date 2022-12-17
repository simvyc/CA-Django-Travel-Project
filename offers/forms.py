from django import forms
from .models import ReviewAndRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewAndRating
        fields = ['subject', 'review', 'rating']