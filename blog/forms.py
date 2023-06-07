from django import forms
from .models import Review, Rating
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class ReviewForm(forms.ModelForm):
    """
    Form for creating or updating reviews.
    """

    class Meta:
        model = Review
        fields = ['title', 'body']

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and customize the widget attributes.
        """
        super().__init__(*args, **kwargs)

        # Customize the widget attributes for the 'title' field
        self.fields['title'].widget.attrs['placeholder\
            '] = 'Give your review a title'
        self.fields['title'].widget.attrs['value\
            '] = self.instance.title if self.instance else ''

        # Customize the widget attributes for the 'body' field
        self.fields['body'].widget.attrs['placeholder\
            '] = 'Write your review here'
        self.fields['body'].widget.attrs['value\
            '] = self.instance.body if self.instance else ''

        # Remove labels from all form fields
        for field_name, field in self.fields.items():
            field.label = ''

        # Create a FormHelper instance and customize the widget
        # attributes for all form fields
        self.helper = FormHelper()


class StarRatingWidget(forms.widgets.Widget):
    """
    A custom widget for rendering star ratings as radio buttons.
    """

    def render(self, name, value, attrs=None, renderer=None):
        """
        Renders the widget as HTML.
        """
        html = ''
        for i in range(1, 6):
            checked = 'checked' if str(i) == str(value) else ''
            html += (
                f'<label><input type="radio" name="{name}" value="{i}" '
                f'{checked} style="display: none;" '
                f'onchange="this.form.submit();" /> '
                f'<i class="fas fa-star rating-form" aria-hidden="true" '
                f'style="cursor: pointer;"> '
                f'</i><button class="magic-button" type="submit" '
                f'name="select_rating" style="display: none;">'
                f'</button></label>'
            )
        return html


class RatingForm(forms.ModelForm):
    """
    Form for rating a product.
    """

    rating = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 6)],
        widget=StarRatingWidget(attrs={'class': 'star-rating'}),
        label='Rate this product:'
    )

    class Meta:
        model = Rating
        fields = ['rating']

    def __init__(self, *args, **kwargs):
        """
        Initializes the form and customizes the form layout.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('rating', css_class='star-rating'),
            Submit('submit', 'Submit')
        )
