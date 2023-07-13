from django.shortcuts import render, redirect
from .models import Player, Game, Score


def home(request):
    return render(request, 'home.html')


def game(request):
    if not request.user.is_authenticated:
        return redirect('login')

    player = Player.objects.get(user=request.user)
    game = Game.objects.create(player=player, board_width=20, board_height=20)
    game.initialize_snake(initial_length=4)
    game.generate_food()

    context = {
        'player': player,
        'game': game,
    }
    return render(request, 'game.html', context)


def login(request):
    return render(request, 'login.html')


def leaderboard(request):
    scores = Score.objects.order_by('-score')[:10]
    context = {
        'scores': scores,
    }
    return render(request, 'leaderboard.html', context)
