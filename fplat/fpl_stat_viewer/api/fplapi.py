import requests
import json
import sys

def request_all_data():

    # get the main data, including data from this season and historic data.
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")

    # check the http error code is 200 (ok).
    if response.status_code is not 200:
        print("couldn't get data. http error code: {}".format(response.status_code))
        sys.exit()

    # convert to json.
    response = response.json()

    # return the json response.
    return response

def request_player_data(player_id):

    # get the player data.
    response = requests.get("https://fantasy.premierleague.com/api/element-summary/{0}/".format(player_id))

    # check the http error code is 200 (ok).
    if response.status_code is not 200:
        print("couldn't get data. http error code: {}".format(response.status_code))
        sys.exit()

    # convert to json
    response = response.json()

    # return the json response.
    return response

def request_player_image(player_id):

    all_data = request_all_data()
    for element in all_data["elements"]:
        if element["id"] == player_id:
            return "https://resources.premierleague.com/premierleague/photos/players/110x140/p{0}.png".format(element["code"])
