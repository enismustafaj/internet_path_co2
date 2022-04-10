import requests
import re
import constants

from time import sleep
from exceptions import APIFailException


def parse_output(output):
    hops = re.findall(constants.IP_V4_REGEX, output)
    return hops[1:]


def read_filesites(source_file):

    with open(source_file, "r") as file:
        sites = file.read().split("\n")
        return sites


def get_location_from_ip(endpoint, headers=None, params=None):
    response = requests.get(endpoint, headers=headers, params=params)
    response = response.json()

    if 'latitude' in response and 'longitude' in response:
        return (response['latitude'], response['longitude'])
    elif 'location' in response:
        return (response['location']['latitude'],
                response['location']['longitude'])
    else:
        return ()


def get_carbon_intensity(endpoint, headers=None, params=None):
    response = requests.get(endpoint, headers=headers, params=params)
    response = response.json()

    if 'message' in response:
        if response['message'] == 'API rate limit exceeded':
            sleep(1)
            return get_carbon_intensity(endpoint,
                                        headers=headers,
                                        params=params)
        else:
            raise APIFailException(response['message'])
    else:
        return response['data']['carbonIntensity']
