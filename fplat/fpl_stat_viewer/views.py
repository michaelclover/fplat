from django.shortcuts import render
from fpl_stat_viewer import fplapi

def index(request):

    args = {"player_data": fplapi.request_all_data()}
    return render(request, 'index.html', args)
