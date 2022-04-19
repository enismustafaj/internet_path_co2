import subprocess
import os
import platform
import argparse

from dotenv import load_dotenv
import constants
import utils

load_dotenv()

arg_parser = argparse.ArgumentParser(
    description="A tool to mesasure CO2 impact of internet route"
)
arg_parser.add_argument("--source", help="Provide source file of websites")
arg_parser.add_argument("--command", help="Provide traceroute command")

args = arg_parser.parse_args()

if __name__ == "__main__":

    website_carbon = dict()

    if args.command:
        trace_command = args.command.split(" ")
    else:
        if platform.system() == "Windows":
            trace_command = ["tracert"]
        else:
            trace_command = ["traceroute"]

    if args.source:
        sites = utils.read_filesites(args.source)
    else:
        sites = utils.read_filesites("./topsites.txt")

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

        hops = utils.parse_output(routes.stdout)

        geolocations = []
        countries = []
        for hop in hops:
            try:
                location, country_code = utils.get_location_from_ip(
                    constants.IP_DATA_ENDPOINT % hop,
                    None,
                    {"api-key": os.getenv("IP_DATA_API_KEY")},
                )
                geolocations.append(location)
                countries.append(country_code)
                print(hop, ": ", location, " - ", country_code)
            except utils.APIFailException as e:
                print(e)

        carbon_intensities = []

        for i, location in enumerate(geolocations):
            if not len(location) == 0:
                try:
                    carbon_intensities.append(
                        utils.get_carbon_intensity(
                            constants.CO2_SIGNAL_ENDPOINT,
                            headers={"auth-token": os.getenv("CO2_SIGNAL_API_KEY")},
                            params={"lat": location[0], "lon": location[1]},
                        )
                    )
                except utils.APIFailException as e:
                    carbon_intensities.append(-1)
                    print(e)

        website_carbon[site] = {
            "hops": hops,
            "carbon_intensities": carbon_intensities,
            "countries": countries,
        }
        print("Traceroute for ", site, " completed")
        utils.print_results_to_file(website_carbon)
