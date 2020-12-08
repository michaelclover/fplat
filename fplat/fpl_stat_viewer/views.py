from django.shortcuts import render
from fpl_stat_viewer.api import fplapi

def index(request):
    args = {"player_data": fplapi.request_all_data()}
    return render(request, 'index.html', args)

def player(request, player_id):
    player_data = fplapi.request_player_data(player_id)
    player_img = fplapi.request_player_image(player_id)

    args = {"player_data": player_data,
            "player_img": player_img}
    return render(request, 'player.html', args)
