from django.conf import settings

import requests
import json
import sys

def request_player_data(player_id):

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

    # search for the player_id using the player_code in order to format the img url, then return it.
    with open("{0}/data/fplapi.json".format(settings.BASE_DIR)) as json_file:
        response = json.load(json_file)
        for element in response["elements"]:
            if element["id"] == player_id:
                return "https://resources.premierleague.com/premierleague/photos/players/110x140/p{0}.png".format(element["code"])
