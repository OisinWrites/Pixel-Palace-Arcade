from django import forms
from .models import Review, Rating


class ReviewForm(forms.ModelForm):
    # title = forms.CharField(max_length=255)
    # body = forms.Textarea()
    # rating = forms.IntegerField()

    class Meta:
        model = Review
        fields = [
            'title',
            'body',
            'aggregate_rating',
        ]


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating']
