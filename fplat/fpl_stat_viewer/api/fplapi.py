from django.conf import settings

import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import sys
import io
import urllib
import base64

def request_player_data(player_id):

    # returns the requested player_id data as json.
    # this is the data as returned by the below request to the FPLAPI with a couple of
    # additions, including the player image url.

    # get the player data.
    response = requests.get("https://fantasy.premierleague.com/api/element-summary/{0}/".format(player_id))

    # check the http error code is 200 (ok).
    if response.status_code is not 200:
        print("couldn't get data. http error code: {}".format(response.status_code))
        sys.exit()

    # convert response to json
    response = response.json()

    # find the player element in the primary API call.
    with open("{0}/data/fplapi.json".format(settings.BASE_DIR)) as json_file:

        scnd_response = json.load(json_file)

        for element in scnd_response["elements"]:
            if element["id"] == player_id:
                response["element"] = element
                break

        response["img_url"] = request_player_image(player_id)

    # return the json response.
    return response

def request_player_image(player_id):

    # returns the url linking to the image of the player.

    # search for the player_id using the player_code in order to format the img url, then return it.
    with open("{0}/data/fplapi.json".format(settings.BASE_DIR)) as json_file:
        response = json.load(json_file)
        for element in response["elements"]:
            if element["id"] == player_id:
                return "https://resources.premierleague.com/premierleague/photos/players/110x140/p{0}.png".format(element["code"])

def request_player_data_as_plot(player_id, data=None, plot=None):

    # returns the requested data in the requested plot.
    # the default is a basic x,y plot returning data from the previous five fixtures.

    fig, ax = plt.subplots()
    data = request_player_data(player_id)

    # get the points from the previous five games for this player.
    count = 0
    last_five = []
    x = []
    player_fixture_history = data["history"]
    player_fixture_history.reverse()
    for j in player_fixture_history:
        last_five.append(j["total_points"])
        x.append(j["round"])
        count = count + 1
        if count > 4:
            break

    ax.plot(x, last_five)
    ax.set(xlabel="gameweek", ylabel="points", title="")
    ax.grid(False)

    #plt.plot(range(10))
    plt.yticks(np.arange(min(last_five), max(last_five)+1, 1))
    plt.xticks(np.arange(min(x), max(x)+1, 1))
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri
