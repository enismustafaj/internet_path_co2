import pandas as pd
import os
import json

import matplotlib.pyplot as plt


arg_parser = argparse.ArgumentParser(
    description="A tool to mesasure CO2 impact of internet route"
)
arg_parser.add_argument("--source", help="Provide source directory")
arg_parser.add_argument("-h", "--hops", action="store_true")
arg_parser.add_argument("-c", "--carbon", action="store_true")
arg_parser.add_argument("--output", help="Provide output file")

args = arg_parser.parse_args()


def create_json_output(runs, content):
    for key, value in content.items():
        new_values = [
            len(value["hops"]),
            sum(value["carbon_intensities"]),
            len([x for x in value["carbon_intensities"] if x == -1]),
        ]
        if key in runs:
            runs[key] += new_values

        else:
            runs[key] = new_values

    return runs


def create_csv_output(runs, content):
    pass


def extract_carbon_emission(df):
    carbon_emission = []

    for head in df.columns.tolist():
        if head[0] == "Carbon Emission" or head[1] == "Carbon Emission":
            carbon_emission.append(head)

    return df[carbon_emission]


def extract_hops(df):
    hops = []

    for head in df.columns.tolist():
        if head[0] == "Hops" or head[1] == "Hops":
            hops.append(head)

    return df[hops]


def export_data(source):
    nr_of_runs = len(os.listdir(source))
    main_cols = ["Run " + str(i) for i in range(1, nr_of_runs + 1)]
    sec_cols = ["Hops", "Carbon Emission", "Error Carbon Val"]
    cols = pd.MultiIndex.from_product([main_cols, sec_cols])

    runs = dict()
    for i, file in enumerate(os.listdir(source)):
        with open(source + "/" + file, "r") as f:
            content = json.load(f)
            runs = create_json_output(runs, content)
    values = []

    for key, value in runs.items():
        values.append(value)

    df = pd.DataFrame(values, columns=cols, index=runs.keys())

    df["Destination"] = df.index.to_numpy().flatten()

    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]


if __name__ == "__main__":
    df = export_data(args.source)

    if args.carbon:
        df = extract_carbon_emission(df)
    elif args.hops:
        df = extract_hops(df)

    fig, ax = plt.subplots(1, 1, figsize=(20, 15))

    fig.patch.set_visible(False)
    ax.axis("off")
    ax.axis("tight")
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
    )
    fig.tight_layout()
    fig.savefig(args.output)
