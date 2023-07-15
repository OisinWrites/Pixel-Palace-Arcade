from django.db import models
from profiles.models import Avatar
from django.contrib.auth.models import User
import random


class Player(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE,
                               null=True, blank=True)
    games_played = models.PositiveIntegerField(default=0)
    highscore = models.PositiveIntegerField(default=0)


class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    board_width = models.PositiveIntegerField()
    board_height = models.PositiveIntegerField()
    snake_body = models.TextField(default='')
    food_position_row = models.PositiveIntegerField()
    food_position_col = models.PositiveIntegerField()
    direction = models.CharField(max_length=10, default='right')
