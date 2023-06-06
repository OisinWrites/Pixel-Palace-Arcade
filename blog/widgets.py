from django import forms


class RatingWidget(forms.TextInput):
    template_name = 'blog/custom_widget_templates/rating_widget.html'

    class Media:
        css = {
            'all': ('blog/static/blog/css/blog.css',),
        }
        js = ('blog/js/star_rating.js',)

    def format_value(self, value):
        if value is None:
            return ''
        return str(value)
