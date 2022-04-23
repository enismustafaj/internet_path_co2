import json
import os
import requests
import re
import constants
import csv
import subprocess

from time import sleep
from exceptions import APIFailException
from datetime import datetime


def parse_output(output):
    hops = re.findall(constants.IP_V4_REGEX, output)

    if len(hops) == 0:
        return []

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


def get_carbon_intensity(endpoint, state, params=None):

    headers = {"auth-token": state.get_token_state()}
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response = response.json()
        print(response)
    except requests.exceptions.RequestException as e:
        raise APIFailException(e)

    if "message" in response:
        if response["message"] == "API rate limit exceeded":
            state.update_token_state()
            sleep(35)
            return get_carbon_intensity(endpoint, state, params=params)
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
        f"{path}/results_" + now.strftime("%m_%d_%Y") + filename + ".json", "w+"
    ) as file:
        file.write(json.dumps(results))


def traceroute_sites(sites, loop, output, trace_command, state):
    website_carbon = dict()
    for i, site in enumerate(sites):

        print("Tracerouting ", site, " ...")
        routes = subprocess.run(
            trace_command + [site],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if routes.returncode != 0:
            print(f"Traceroute for {site} failed")
            continue

        hops = parse_output(routes.stdout)

        geolocations = []
        countries = []
        for hop in hops:
            try:
                location, country_code = get_location_from_ip(
                    constants.IP_DATA_ENDPOINT % hop,
                    None,
                    {"api-key": os.getenv("IP_DATA_API_KEY")},
                )
                geolocations.append(location)
                countries.append(country_code)
                print(hop, ": ", location, " - ", country_code)
            except APIFailException as e:
                print(e)

        carbon_intensities = []

        for i, location in enumerate(geolocations):
            if not len(location) == 0:
                try:
                    carbon_intensities.append(
                        get_carbon_intensity(
                            constants.CO2_SIGNAL_ENDPOINT,
                            state,
                            params={"lat": location[0], "lon": location[1]},
                        )
                    )
                except APIFailException as e:
                    carbon_intensities.append(-1)
                    print(e)

        website_carbon[site] = {
            "hops": hops,
            "carbon_intensities": carbon_intensities,
            "countries": countries,
        }
        print("Traceroute for ", site, " completed")
        print_results_to_file(
            website_carbon, filename="_loop" + str(loop) + "_" + output
        )
