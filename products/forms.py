from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating products in a crispy form.
    Styled to fit app, custom labels.
    Uses custom widget to tidy image upload field.
    """

    class Meta:
        model = Product
        fields = ['price', 'image_url', 'image', 'name',
                  'category', 'description', 'has_variants']

    image = forms.ImageField(label='Image', required=False,
                             widget=CustomClearableFileInput,)

    price = forms.DecimalField(label='Price', max_digits=6, decimal_places=2,
                               widget=forms.NumberInput(
                                attrs={'placeholder': 'Enter price...'}))

    image_url = forms.URLField(label='Image URL', max_length=1824,
                               widget=forms.TextInput(
                                attrs={'placeholder': 'Enter image URL...'}))

    name = forms.CharField(label='Product Name', max_length=254,
                           widget=forms.TextInput(
                            attrs={'placeholder': 'Enter product name...'}))

    category = forms.ModelChoiceField(
        label='Category', queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'rounded-1'}))

    description = forms.CharField(
        label='Description', widget=forms.Textarea(
            attrs={'placeholder': 'Enter product description...'}))

    has_variants = forms.BooleanField(
        label='Has Variants', required=False,
        widget=forms.CheckboxInput(attrs={'class': 'rounded-1'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded-1'
