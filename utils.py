import json
import os
import requests
import re
import constants
import csv

from time import sleep
from exceptions import APIFailException
from datetime import datetime


def parse_output(output):
    hops = re.findall(constants.IP_V4_REGEX, output)

    if hops[0] == hops[len(hops) - 1]:
        return hops[1:]
    else:
        return hops


def read_filesites(source_file):

    try:
        with open(source_file, "r") as file:
            sites = []
            rows = csv.reader(file, delimiter=",")
            if check_header(file):
                next(rows, None)
            for row in rows:
                sites.append(row[0])

            return sites
    except FileNotFoundError:
        raise Exception("File not found")


def check_header(file):
    first = file.read(1)
    return first in "abcdefghijklmopqrstuvwxyz"


def get_location_from_ip(endpoint, headers=None, params=None):
    response = requests.get(endpoint, headers=headers, params=params)
    response = response.json()

    if "latitude" in response and "longitude" in response:
        return (response["latitude"], response["longitude"]), response["country_code"]
    elif "location" in response:
        return (
            response["location"]["latitude"],
            response["location"]["longitude"],
        ), response["country_code"]
    else:
        raise APIFailException("No location found")


def get_carbon_intensity(endpoint, headers=None, params=None):
    response = requests.get(endpoint, headers=headers, params=params)
    response = response.json()
    print(response)

    if "message" in response:
        if response["message"] == "API rate limit exceeded":
            sleep(50)
            return get_carbon_intensity(endpoint, headers=headers, params=params)
        else:
            raise APIFailException(response["message"])
    else:
        if "data" in response and "carbonIntensity" in response["data"]:
            return response["data"]["carbonIntensity"]
        else:
            raise APIFailException("No data found")


def print_results_to_file(results, path="./results", filename=""):
    now = datetime.now()

    dir_exists = os.path.exists(path)
    if not dir_exists:
        os.mkdir(path)

    with open(
        f"{path}/results_json_" + now.strftime("%m_%d_%Y") + filename + ".json", "w+"
    ) as file:
        file.write(json.dumps(results))
