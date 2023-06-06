from django import forms


class RatingWidget(forms.TextInput):
    template_name = 'blog/custom_widget_templates/rating_widget.html'

    class Media:
        css = {
            'all': ('rating_widget.css',)  # Add CSS styles for the widget
        }
        js = ('rating_widget.js',)  # Add JavaScript for the widget

    def format_value(self, value):
        if value is None:
            return ''
        return str(value)

