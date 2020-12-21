import requests
import json
import sys

def request_all_data(add_extra_data=True):

    # get the main data, including data from this season and historic data.
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")

    # check the http error code is 200 (ok).
    if response.status_code is not 200:
        print("couldn't get data. http error code: {}".format(response.status_code))
        sys.exit()

    # convert response to json.
    response = response.json()

    if add_extra_data:

        # convert the team IDs to team names for displaying.
        teamMap = {}
        for teams in response["teams"]:
            if teams["code"] not in teamMap:
                teamMap[teams["code"]] = teams["name"]

        # convert the position IDs to position names for displaying.
        positionMap = {}
        for position in response["element_types"]:
            if position["id"] not in positionMap:
                positionMap[position["id"]] = position["singular_name"]

        # update the player json with better formatted data from above etc.
        for element in response["elements"]:
            element["team_code"] = teamMap[element["team_code"]]
            element["element_type"] = positionMap[element["element_type"]]
            element["start_price"] = element["now_cost"] - element["cost_change_start"]
            element["start_price"] = str(element["start_price"])[:-1] + "." + str(element["start_price"])[-1]
            element["now_cost"] = str(element["now_cost"])[:-1] + "." + str(element["now_cost"])[-1] # convert int to decimal to reflect player price. e.g. 69 to 6.9. for £6.9 million.

            # check the news strings to determine whether we should signal the view to red or yellow flag players.
            if "Unknown return date".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "Transferred to".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "Suspended until".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "Expected back".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "Left the club".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "on a permanent deal".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "Contract terminated".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "Contract expired".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "Contract ended".upper() in element["news"].upper():
                element["alert"] = "red"
            elif "Chance of playing".upper() in element["news"].upper():
                element["alert"] = "yellow"

    # return the json response.
    return response

def request_player_data(player_id, add_extra_data=True):

    # get the player data.
    response = requests.get("https://fantasy.premierleague.com/api/element-summary/{0}/".format(player_id))

    # check the http error code is 200 (ok).
    if response.status_code is not 200:
        print("couldn't get data. http error code: {}".format(response.status_code))
        sys.exit()

    # convert response to json
    response = response.json()

    # get extra data, such as the player's name etc.
    if add_extra_data:

        # find the player element in the primary API call.
        scnd_response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")

        # check the http error code is 200 (ok).
        if scnd_response.status_code is not 200:
            print("couldn't get data. http error code: {}".format(scnd_response.status_code))
            sys.exit()

        # convert response to json
        scnd_response = scnd_response.json()

        for element in scnd_response["elements"]:
            if element["id"] == player_id:
                response["element"] = element
                break

        response["img_url"] = request_player_image(player_id)

    # return the json response.
    return response

def request_player_image(player_id):

    # search for the player_id using the player_code in order to format the img url, then return it.
    response = request_all_data(add_extra_data=False)
    for element in response["elements"]:
        if element["id"] == player_id:
            return "https://resources.premierleague.com/premierleague/photos/players/110x140/p{0}.png".format(element["code"])
