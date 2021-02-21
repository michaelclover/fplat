from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseNotFound
from fpl_stat_viewer.api import fplapi

import json

def index(request):
    try:
        with open("{0}/data/fplapi.json".format(settings.BASE_DIR)) as json_file:
            data = json.load(json_file)
            args = {"player_data": data}
            return render(request, 'index.html', args)
    except IOError:
        return HttpResponseNotFound("404 - Couldn't retrieve data.")

def player(request, player_id):
    args = {"player_data": fplapi.request_player_data(player_id),
            "player_plot": fplapi.request_player_data_as_plot(player_id)}
    return render(request, 'player.html', args)
