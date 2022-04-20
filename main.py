import platform
import argparse

from dotenv import load_dotenv
import utils

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
        sites = utils.read_filesites(args.source)
    else:
        sites = utils.read_filesites("./topsites.txt")

    if args.loop:
        loop = int(args.loop)
    else:
        loop = 1

    if args.output:
        output_file = args.output
    else:
        output_file = ""

    for i in range(loop):

        utils.traceroute_sites(sites, i + 1, output_file, trace_command)
