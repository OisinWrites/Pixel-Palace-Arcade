from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Player, Game, Score
from profiles.models import Avatar, UserProfile
from .snake_logic import SnakeGame


@login_required
def game(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    avatar = Avatar.objects.filter(user=profile.user).first()
    player, created = Player.objects.get_or_create(user=request.user)
    game = Game.objects.create(player=player, board_width=20, board_height=20,
                               food_position_row=0, food_position_col=0)

    # Create an instance of the SnakeGame class
    snake_game = SnakeGame(
        board_width=game.board_width, board_height=game.board_height)

    # Initialise the game
    snake_game.initialise_game(initial_length=4)
    snake_game.generate_food()

    context = {
        'player': player,
        'game': game,
        'avatar': avatar,
    }
    return render(request, 'snake/snake.html', context)


def leaderboard(request):
    scores = Score.objects.order_by('-score')[:10]
    context = {
        'scores': scores,
    }
    return render(request, 'leaderboard.html', context)
