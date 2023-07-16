from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Player, Game
from .forms import PlayerNameForm
from profiles.models import Avatar
from django.http import JsonResponse


def update_player_name(player, avatar):
    # If an avatar exists, use the associated user's
    # username as the player name
    if avatar:
        player.name = avatar.user.username
    elif player.user:
        # If no avatar but the user exists,
        # use the user's username as the player name
        player.name = player.user.username
    else:
        # If neither avatar nor user exists,
        # use the custom player name field
        player.name = player.avatar_name
    player.save()


def game(request):
    # Fetch the current user's player data
    if request.user.is_authenticated:
        try:
            player = Player.objects.get(user=request.user)
        except Player.DoesNotExist:
            player = Player.objects.create(user=request.user)

        # Fetch the associated avatar if available
        try:
            avatar = Avatar.objects.get(user=request.user)
        except Avatar.DoesNotExist:
            avatar = None

        # Update the player's name based on the avatar information
        update_player_name(player, avatar)

    else:
        # For anonymous users, create a new player instance
        player = Player.objects.create()

    game_board = [['empty' for _ in range(12)] for _ in range(9)]
    game_board[4][6] = 'snake-head'

    # Enumerate the rows and columns to pass to the template
    rows = range(len(game_board))
    cols = range(len(game_board[0]))

    context = {
        'game_board': game_board,
        'rows': rows,
        'cols': cols,
        'player': player,
    }

    return render(request, 'snake/snake.html', context)
