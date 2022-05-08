import platform
import argparse
import os
import utils
import export

from dotenv import load_dotenv
from exceptions import ReadFileException
from token_state import TokenState

load_dotenv()

# Declare the arguments
arg_parser = argparse.ArgumentParser(
    description="A tool to mesasure CO2 impact of internet route"
)
arg_parser.add_argument("--source", help="Provide source file of websites")
arg_parser.add_argument("--command", help="Provide traceroute command")
arg_parser.add_argument("--loop", help="Provide number of runs")
arg_parser.add_argument("--output", help="Provide output file")
arg_parser.add_argument("--export", help="Export results to csv")

# Parsing arguments
args = arg_parser.parse_args()

if __name__ == "__main__":

    # Check if the source file is provided
    if not args.source:
        print("No source file provided")
        exit(1)

    if args.output:
        output_file = args.output
    else:
        output_file = ""

    if args.export:
        output_path = "./data"
        export.export_data(args.source, output_file, output_path, args.export, True)

    else:

        output_path = "./result"
        website_carbon = dict()

        try:
            sites = utils.read_csv_file(args.source)
        except ReadFileException as e:
            print(e)
            exit(1)

        # Set the trace command
        if args.command:
            trace_command = args.command.split(" ")
        else:
            if platform.system() == "Windows":
                trace_command = ["tracert"]
            else:
                trace_command = ["traceroute"]

        # Set the number of runs
        if args.loop:
            loop = int(args.loop)
        else:
            loop = 1

        # Add tokens and initialize the token state
        tokens = [
            os.getenv("CO2_SIGNAL_API_KEY"),
            os.getenv("CO2_SIGNAL_API_KEY2"),
            os.getenv("CO2_SIGNAL_API_KEY3"),
            os.getenv("CO2_SIGNAL_API_KEY4"),
        ]
        state = TokenState(tokens, 0)

        # Loop through the input sites
        for i in range(loop):

            utils.traceroute_sites(
                sites, i + 1, output_file, output_path, trace_command, state
            )
