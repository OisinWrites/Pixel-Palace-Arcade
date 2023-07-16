from django import forms
from .models import Player


class PlayerNameForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['player_name']
