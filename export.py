import os
import json
import utils
import constants
import math

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Create a json output from the dataframe
def create_json_output(runs, content):
    for key, value in content.items():
        new_values = [
            len(value["hops"]),
            sum(value["carbon_intensities"]),
            len([x for x in value["carbon_intensities"] if x == -1]),
            len([x for x in value["countries"] if x == ""]),
        ]
        if key in runs:
            runs[key] += new_values
        else:
            runs[key] = new_values

    return runs


# Output a csv file from the dataframe
def create_csv_output(df, output):
    pd.DataFrame.to_csv(df, output, index=False)


# Extract column types from the dataframe
def extract_columns(df, column_name):
    hops = []
    hops.append(df.columns.tolist()[0])

    for head in df.columns.tolist():
        if head[0] == column_name or head[1] == column_name:
            hops.append(head)

    return df[hops]


# Create a dataframe from the source file
def create_data_frame(source):
    nr_of_runs = len(os.listdir(source))

    # Set the columns
    main_cols = ["Run " + str(i) for i in range(1, nr_of_runs + 1)]
    sec_cols = ["Hops", "Carbon Emission", "Error Carbon Val", "Error lookup"]
    cols = pd.MultiIndex.from_product([main_cols, sec_cols])

    # Process the data from each file
    runs = dict()
    for i, file in enumerate(os.listdir(source)):
        with open(source + "/" + file, "r") as f:
            content = json.load(f)
            runs = create_json_output(runs, content)
    values = []

    for key, value in runs.items():
        values.append(value)

    df = pd.DataFrame(values, columns=cols, index=runs.keys())

    # Add the destination column
    df["Destination"] = df.index.to_numpy().flatten()

    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    return df


# Plot the graph
def plot_graph(df, graph_file, type, sort=False):

    if type == "lookup_error":
        df["sum. round1"] = df.iloc[:, 1:4].sum(axis=1)
        df["sum. round2"] = df.iloc[:, 4:7].sum(axis=1)
    else:
        df["avg. round1"] = df.iloc[:, 1:4].mean(axis=1)
        df["avg. round2"] = df.iloc[:, 4:7].mean(axis=1)

    df["difference"] = abs(df["avg. round1"] - df["avg. round2"])
    print(df["difference"].max())
    print(df["difference"].mean())
    dest = df.iloc[:, 0]
    if sort:
        df = df.sort_values(by=("avg. round2", ""))

    max1 = df[("avg. round1", "")].max()
    max2 = df[("avg. round2", "")].max()
    max_value = max(max1, max2)

    X_axis = np.arange(len(dest))

    y_label = constants.GRAPH_LABELS[type]

    plt.figure(figsize=(15, 15))
    plt.xticks(X_axis, dest, rotation=90)
    plt.xlabel(constants.GRAPH_LABELS["x_label"])
    plt.ylabel(y_label)
    if type == "lookup_error":
        plt.ylim([0, math.ceil(max_value) + 1])
    plt.bar(X_axis - 0.2, df["avg. round1"], 0.4, label="Round 1")
    plt.bar(X_axis + 0.2, df["avg. round2"], 0.4, label="Round 2")
    plt.legend()
    plt.show()
    plt.savefig(graph_file + ".pdf", dpi=300, bbox_inches="tight")


# Export the dataframe to a csv file
def export_data(source, output_file, output_path, type, sort, csv=False):
    df = create_data_frame(source)

    utils.create_res_dir(output_path)

    # Check the type of export
    if type in constants.EXPORT_TYPE:
        df = extract_columns(df, constants.EXPORT_TYPE[type])
    else:
        print("Invalid type")
        exit(1)

    plot_graph(df, output_file, type, sort=sort)
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))

    fig.patch.set_visible(False)
    ax.axis("off")
    ax.axis("tight")
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
    )
    fig.tight_layout()
    fig.savefig(output_path + "/" + output_file)

    if csv:
        create_csv_output(df, output_path + "/" + output_file)
