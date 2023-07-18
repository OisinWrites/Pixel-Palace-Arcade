from django import forms


class MarkOrderCompletedForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput())
