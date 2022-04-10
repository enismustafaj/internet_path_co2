import subprocess
import os
import platform
import argparse
from time import sleep

from dotenv import load_dotenv
import constants
import utils

load_dotenv()

arg_parser = argparse.ArgumentParser(
    description='A tool to mesasure CO2 impact of internet route')
arg_parser.add_argument('--source', help='Provide source file of websites')
arg_parser.add_argument('--command', help='Provide traceroute command')

args = arg_parser.parse_args()

if __name__ == '__main__':

    website_carbon = dict()

    if args.command:
        trace_command = args.command
    else:
        if platform.system() == "Windows":
            trace_command = "tracert"
        else:
            trace_command = "traceroute"

    if args.source:
        sites = utils.read_filesites(args.source)
    else:
        sites = utils.read_filesites('./topsites.txt')

    for i, site in enumerate(sites):
        if i == 1:
            break
        print("Trecerouting ", site, " ...")
        routes = subprocess.run([trace_command, site],
                                stdout=subprocess.PIPE,
                                text=True)
        hops = utils.parse_output(routes.stdout)

        geolocations = []
        for hop in hops:
            geolocations.append(
                utils.get_location_from_ip(
                    constants.IP_DATA_ENDPOINT % hop, None,
                    {'api-key': os.getenv('IP_DATA_API_KEY')}))

        carbon_intensities = []

        for i, location in enumerate(geolocations):
            if not len(location) == 0:
                try:
                    carbon_intensities.append(
                        utils.get_carbon_intensity(
                            constants.CO2_SIGNAL_ENDPOINT,
                            headers={
                                'auth-token': os.getenv('CO2_SIGNAL_API_KEY')
                            },
                            params={
                                'lat': location[0],
                                'lon': location[1]
                            }))
                except utils.APIFailException as e:
                    print(e)

        website_carbon['site'] = carbon_intensities

    print(carbon_intensities)
