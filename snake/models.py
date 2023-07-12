from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_name = models.CharField(max_length=255)
    games_played = models.PositiveIntegerField(default=0)
    highscore = models.PositiveIntegerField(default=0)
