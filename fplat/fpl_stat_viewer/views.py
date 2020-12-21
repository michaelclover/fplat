from django.shortcuts import render
from fpl_stat_viewer.api import fplapi

def index(request):
    args = {"player_data": fplapi.request_all_data()}
    return render(request, 'index.html', args)

def player(request, player_id):
    args = {"player_data": fplapi.request_player_data(player_id)}
    return render(request, 'player.html', args)
