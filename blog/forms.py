from django import forms
from .models import Review, Rating
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder\
            '] = 'Give you review a title'
        self.fields['title'].widget.attrs['value\
            '] = self.instance.title if self.instance else ''
        self.fields['body'].widget.attrs['placeholder\
            '] = "Write your review here"
        self.fields['body'].widget.attrs['value\
            '] = self.instance.body if self.instance else ''
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='border-black rounded-0'),
            Field('body', css_class='border-black rounded-0'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )


class StarRatingWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = ''
        for i in range(1, 6):
            checked = 'checked' if str(i) == str(value) else ''
            html += f'<label><input type="radio" name="{name}" value="{i}" \
                {checked} style="display: none;" \
                    onchange="this.form.submit();" /> \
                <i class="fas fa-star rating-form" aria-hidden="true" \
                    style="cursor: pointer;"> \
                </i><button class="magic-button" type="submit" \
                    name="select_rating" style="display: none;"> \
                    </button></label>'
        return html


class RatingForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=StarRatingWidget(attrs={'class': 'star-rating'}),
        label='Rate this product:'  # Custom label for the rating field
    )

    class Meta:
        model = Rating
        fields = ['rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('rating', css_class='star-rating'),
            Submit('submit', 'Submit')
        )
