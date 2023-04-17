from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    # title = forms.CharField(max_length=255)
    # body = forms.Textarea()
    # rating = forms.IntegerField()

    class Meta:
        model = Review
        fields = [
            'title',
            'body',
            'rating',
        ]
