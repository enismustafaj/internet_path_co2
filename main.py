import platform
import argparse
import os

from dotenv import load_dotenv
from exceptions import ReadFileException
import utils
from token_state import TokenState

load_dotenv()

arg_parser = argparse.ArgumentParser(
    description="A tool to mesasure CO2 impact of internet route"
)
arg_parser.add_argument("--source", help="Provide source file of websites")
arg_parser.add_argument("--command", help="Provide traceroute command")
arg_parser.add_argument("--loop", help="Provide number of runs")
arg_parser.add_argument("--output", help="Provide output file")


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
        try:
            sites = utils.read_csv_file(args.source)
        except ReadFileException as e:
            print(e)
            exit(1)
    else:
        sites = utils.read_csv_file("./topsites.txt")

    if args.loop:
        loop = int(args.loop)
    else:
        loop = 1

    if args.output:
        output_file = args.output
    else:
        output_file = ""

    tokens = [
        os.getenv("CO2_SIGNAL_API_KEY"),
        os.getenv("CO2_SIGNAL_API_KEY2"),
        os.getenv("CO2_SIGNAL_API_KEY3"),
        os.getenv("CO2_SIGNAL_API_KEY4"),
    ]
    state = TokenState(tokens, 0)

    for i in range(loop):

        utils.traceroute_sites(sites, i + 1, output_file, trace_command, state)
