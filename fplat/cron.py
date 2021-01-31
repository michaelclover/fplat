import requests
import json
import sys
import os

def get_fpl_latest():

    # get the main data, including data from this season and historic data.
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")

    # check the http error code is 200 (ok).
    if response.status_code is not 200:
        sys.exit()

    # convert response to json.
    response = response.json()

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

    # write to file
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/fplapi.json'), 'w') as f:
        json.dump(response, f, ensure_ascii=False)
