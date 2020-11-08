import requests
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
