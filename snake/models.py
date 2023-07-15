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

    def get_player_name(self):
        if self.avatar:
            # If an avatar exists, use the associated user's
            # username as the player name
            return self.user.username
        elif self.user:
            # If no avatar but the user exists,
            # use the user's username as the player name
            return self.user.username
        else:
            # If neither avatar nor user exists,
            # use the custom player name field
            return self.player_name

    def __str__(self):
        return self.get_player_name()


class Game(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    board_width = models.PositiveIntegerField()
    board_height = models.PositiveIntegerField()
    snake_body = models.TextField(default='')
    food_position_row = models.PositiveIntegerField()
    food_position_col = models.PositiveIntegerField()
    direction = models.CharField(max_length=10, default='right')
