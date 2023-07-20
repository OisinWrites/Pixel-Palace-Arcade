from django import forms
from profiles.models import UserProfile
from django.contrib.auth.models import User
from .models import Subscriber


class MarkOrderCompletedForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput())


class MarkOrderIncompleteForm(forms.Form):
    order_id = forms.IntegerField(widget=forms.HiddenInput())


class MonthYearFilterForm(forms.Form):
    MONTH_CHOICES = [
        ('', 'All'),
        ('1', 'January'),
        ('2', 'February'),
        ('3', 'March'),
        ('4', 'April'),
        ('5', 'May'),
        ('6', 'June'),
        ('7', 'July'),
        ('8', 'August'),
        ('9', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    YEAR_CHOICES = [
        ('', 'All'),
        ('2022', '2022'),
        ('2023', '2023'),
    ]

    HOUR_CHOICES = [
        ('', 'All'),
        ('00', '12 AM'),
        ('01', '1 AM'),
        ('02', '2 AM'),
        ('03', '3 AM'),
        ('04', '4 AM'),
        ('05', '5 AM'),
        ('06', '6 AM'),
        ('07', '7 AM'),
        ('08', '8 AM'),
        ('09', '9 AM'),
        ('10', '10 AM'),
        ('11', '11 AM'),
        ('12', '12 PM'),
        ('13', '1 PM'),
        ('14', '2 PM'),
        ('15', '3 PM'),
        ('16', '4 PM'),
        ('17', '5 PM'),
        ('18', '6 PM'),
        ('19', '7 PM'),
        ('20', '8 PM'),
        ('21', '9 PM'),
        ('22', '10 PM'),
        ('23', '11 PM'),
    ]

    DAY_CHOICES = [
        ('', 'All'),
        ('01', '1st'),
        ('02', '2nd'),
        ('03', '3rd'),
        ('04', '4th'),
        ('05', '5th'),
        ('06', '6th'),
        ('07', '7th'),
        ('08', '8th'),
        ('09', '9th'),
        ('10', '10th'),
        ('11', '11th'),
        ('12', '12th'),
        ('13', '13th'),
        ('14', '14th'),
        ('15', '15th'),
        ('16', '16th'),
        ('17', '17th'),
        ('18', '18th'),
        ('19', '19th'),
        ('20', '20th'),
        ('21', '21st'),
        ('22', '22nd'),
        ('23', '23rd'),
        ('24', '24th'),
        ('25', '25th'),
        ('26', '26th'),
        ('27', '27th'),
        ('28', '28th'),
        ('29', '29th'),
        ('30', '30th'),
        ('31', '31st'),
    ]

    month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
    year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    hour = forms.ChoiceField(choices=HOUR_CHOICES, required=False)
    day = forms.ChoiceField(choices=DAY_CHOICES, required=False)


class NewsletterSubscriptionForm(forms.Form):
    # We will use this form to toggle the newsletter subscription status
    newsletter_subscribed = forms.BooleanField(required=False)

    # This method will initialize the form fields with the user's data
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.email = self.user.email
        subscriber = self.user.subscriber.filter(user=self.user).first()
        initial = {'newsletter_subscribed': subscriber.newsletter_subscribed
                   if subscriber else False}
        super(NewsletterSubscriptionForm, self).__init__(
            initial=initial, *args, **kwargs)
        self.subscriber_instance = subscriber  # Store the subscriber instance

    # This method will save the subscription status to the database
    def save(self):
        newsletter_subscribed = self.cleaned_data['newsletter_subscribed']
        self.subscriber_instance.newsletter_subscribed = newsletter_subscribed
        self.subscriber_instance.save()
