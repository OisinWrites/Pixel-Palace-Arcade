from django import forms
from .models import UserProfile, Avatar
from products.widgets import CustomClearableFileInput
from allauth.account.models import EmailAddress


class UserProfileForm(forms.ModelForm):
    """
    Form to set default shipping/billing info
    """
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs[
                'class'] = 'border-black rounded-0 profile-form-input'
            self.fields[field].label = False


class AvatarForm(forms.ModelForm):
    """
    Form to create alternate personal details for
    social engagement within site.
    """
    avatar_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter player name'}),
        label=''
    )

    image = forms.ImageField(label='Choose your hero', required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AvatarForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'

    def save(self, commit=True):
        instance = super(AvatarForm, self).save(commit=False)

        # Check if the user is already assigned
        if not instance.user_id:
            # Retrieve the logged-in user
            user = self.request.user

            # Assign the user to the instance
            instance.user = user

        if commit:
            instance.save()

        return instance

    class Meta:
        model = Avatar
        fields = ['image', 'avatar_name']
