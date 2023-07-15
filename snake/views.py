from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Player, Game
from profiles.models import Avatar
from django.http import JsonResponse


@login_required
def game(request):
    player = Player.objects.get(user=request.user)
    avatar = Avatar.objects.filter(user=request.user).first()

    # Retrieve the game ID from the session or create a new game
    game_id = request.session.get('game_id')
    if game_id:
        game = Game.objects.get(id=game_id)
    else:
        game = Game.objects.create(
            player=player, board_width=20, board_height=20,
            food_position_row=0, food_position_col=0
        )
        game.initialize_snake(initial_length=4)
        game.generate_food()
        request.session['game_id'] = game.id

    # Prepare the game board state
    game_board = [
        [''] * game.board_width for _ in range(game.board_height)
    ]
    snake_body = game.get_snake_body()
    for row, col in snake_body:
        if 0 <= row < game.board_height and 0 <= col < game.board_width:
            game_board[row][col] = 'X'

    game_board[game.food_position_row][game.food_position_col] = 'O'

    context = {
        'player': player,
        'game': game,
        'avatar': avatar,
        'game_board': game_board,
    }
    return render(request, 'snake/snake.html', context)


def change_direction(request, direction):
    game_id = request.session.get('game_id')

    # Logic to handle the direction change
    game = Game.objects.get(id=game_id)
    game.change_direction(direction)
    game.save()

    # Return a JSON response indicating success or any additional data
    return JsonResponse({'status': 'success'})


def update_game_state(request):
    game_id = request.session.get('game_id')

    # Logic to update the game state
    game = Game.objects.get(id=game_id)
    game.move_snake()

    if game.is_game_over():
        # Game over logic
        game.save()
        return JsonResponse({'status': 'game_over'})

    game.check_food_eaten()
    game.save()

    # Prepare the updated game state response
    game_state = {
        'score': game.score,
        'game_over': False,
        'snake_body': game.get_snake_body(),
        'food_position': (game.food_position_row, game.food_position_col),
    }

    # Return the updated game state as a JSON response
    return JsonResponse(game_state)


def end_game(request):
    game_id = request.session.get('game_id')

    # Logic to end the game
    game = Game.objects.get(id=game_id)
    player = game.player
    player.increment_games_played()
    player.update_highscore(game.score)
    player.save()
    game.delete()

    # Clear the game ID from the session
    request.session.pop('game_id', None)

    # Return a JSON response indicating success or any additional data
    return JsonResponse({'status': 'success'})


def pause_game(request):
    game_id = request.session.get('game_id')

    # Logic to pause/resume the game
    game = Game.objects.get(id=game_id)
    game.toggle_pause()
    game.save()

    return JsonResponse({'status': 'success'})
