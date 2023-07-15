from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Player, Game
from profiles.models import Avatar
from django.http import JsonResponse


def start_game(request):
    if request.user.is_authenticated:
        # If the user is logged in,
        # try to find the corresponding Player model instance
        player, created = Player.objects.get_or_create(user=request.user)
    else:
        # If the user is not logged in,
        # create a new Player instance with no associated user
        player = Player.objects.create()

    return JsonResponse({"message": "Game started successfully!"})
