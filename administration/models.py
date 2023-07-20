from django.contrib.auth.models import User
from django.db import models


class Subscriber(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='subscriber')
    email = models.EmailField()
    newsletter_subscribed = models.BooleanField(default=False)

    def __str__(self):
        return self.email
