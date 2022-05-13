import json
import os
import requests
import re
import constants
import csv
import subprocess

from time import sleep
from exceptions import APIFailException, ReadFileException
from datetime import datetime

# Parse the output of the traceroute command
def parse_output(output):
    hops = []
    no_router_detected = 0
    # Split the output by newline
    output = output.split("\n")[1:]
    for i, line in enumerate(output):
        if len(re.findall(constants.IP_V4_REGEX, line)) > 0:
            hops += re.findall(constants.IP_V4_REGEX, line)
        elif "???" in line:
            no_router_detected += 1

    if len(hops) == 0:
        return hops, no_router_detected

    if hops[0] == hops[len(hops) - 1] and len(hops) > 1:
        return hops[1:], no_router_detected
    else:
        return hops, no_router_detected


# Read the destinations from a file
def read_csv_file(source_file):

    try:
        with open(source_file, "r") as file:
            sites = []
            rows = csv.reader(file, delimiter=",")
            # Skip the header if it exists
            if check_header(file):
                # next(rows, None)
                pass
            for row in rows:
                sites.append(row[0])

            return sites
    except FileNotFoundError:
        raise ReadFileException("File not found")


# Check if the file has a header
def check_header(file):
    first_line = file.readline()
    if (
        len(re.findall(constants.URL_REGEX, first_line)) > 0
        or len(re.findall(constants.IP_V4_REGEX, first_line)) > 0
    ):
        return False
    return True


def get_location_from_ip(endpoint, headers=None, params=None):

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response = response.json()
    except requests.exceptions.RequestException as e:
        raise APIFailException(e)

    if (
        "latitude" in response
        and "longitude" in response
        and "country_code" in response
    ):
        return (response["latitude"], response["longitude"]), response["country_code"]

    elif (
        "latitude" in response
        and "longitude" in response
        and "country_code2" in response
    ):
        return (response["latitude"], response["longitude"]), response["country_code2"]
    elif "location" in response and "country" in response:
        return (
            response["location"]["latitude"],
            response["location"]["longitude"],
        ), response["country"]["isoAlpha2"]
    else:
        raise APIFailException("No location found")


# Fetch the carbon intensity from the API
def get_carbon_intensity(endpoint, state, params=None):

    headers = {"auth-token": state.get_token_state()}

    # Check if the request is successful
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response = response.json()
    except requests.exceptions.RequestException as e:
        raise APIFailException(e)

    if "message" in response:
        # Sleep for 15 seconds to avoid hitting the API too quickly
        if response["message"] == "API rate limit exceeded":
            state.update_token_state()
            sleep(15)
            return get_carbon_intensity(endpoint, state, params=params)
        else:
            raise APIFailException(response["message"])
    else:
        if "data" in response and "carbonIntensity" in response["data"]:
            return response["data"]["carbonIntensity"]
        else:
            # If data was not found, raise an exception
            raise APIFailException("No data found")


# Create the results directory if it does not exist
def create_res_dir(path):
    dir_exists = os.path.exists(path)
    if not dir_exists:
        os.mkdir(path)


# Output the results to a file in JSON format
def print_results_to_file(results, path="./results", filename=""):
    now = datetime.now()

    create_res_dir(path)

    with open(
        f"{path}/results_" + now.strftime("%m_%d_%Y") + filename + ".json", "w+"
    ) as file:
        file.write(json.dumps(results))


def traceroute_sites(sites, loop, output_file, output_path, trace_command, state):
    website_carbon = dict()
    for i, site in enumerate(sites):

        # Check if the site is a valid URL
        # by running a tracerote command
        # and collect all the hops
        print("Tracerouting ", site, "...")
        routes = subprocess.run(
            trace_command + [site],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if routes.returncode != 0:
            print(f"Traceroute for {site} failed")
            continue

        hops, unknown_routers = parse_output(routes.stdout)

        geolocations = []
        countries = []

        # Get the geolocation for each hop
        for hop in hops:
            try:
                location, country_code = get_location_from_ip(
                    constants.IP_DATA_ENDPOINT % hop,
                    None,
                    {
                        "api-key": os.getenv("IP_DATA_API_KEY"),
                    },
                )
                geolocations.append(location)
                countries.append(country_code)
                print(hop, ": ", location, " - ", country_code)
            except APIFailException as e:
                countries.append("")
                print(e)

        carbon_intensities = []

        # Get the carbon intensity for each hop
        for i, location in enumerate(geolocations):
            if not len(location) == 0:
                try:
                    carbon_intensity = get_carbon_intensity(
                        constants.CO2_SIGNAL_ENDPOINT,
                        state,
                        params={"lat": location[0], "lon": location[1]},
                    )
                    carbon_intensities.append(carbon_intensity)
                    print(location, ": ", carbon_intensity)
                except APIFailException as e:
                    carbon_intensities.append(-1)
                    print(e)

        # Add the results to the dictionary
        website_carbon[site] = {
            "hops": hops,
            "carbon_intensities": carbon_intensities,
            "countries": countries,
            "unknown_routers": unknown_routers,
        }
        print("Traceroute for ", site, " completed")

        # Print the results to a file
        print_results_to_file(
            website_carbon,
            output_path,
            filename="_loop" + str(loop) + "_" + output_file,
        )
