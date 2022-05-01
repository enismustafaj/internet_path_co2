import pandas as pd
import os
import json
import utils

import matplotlib.pyplot as plt


# Create a json output from the dataframe
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


# Output a csv file from the dataframe
def create_csv_output(df, output):
    pd.DataFrame.to_csv(df, output, index=False)


# Extract carbon intensities error values from the dataframe
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
    sec_cols = ["Hops", "Carbon Emission", "Error Carbon Val"]
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


# Export the dataframe to a csv file
def export_data(source, output_file, output_path, type, csv=False):
    df = create_data_frame(source)

    utils.create_res_dir(output_path)

    # Check the type of export
    if type == "carbon":
        df = extract_columns(df, "Carbon Emission")
    elif type == "hops":
        df = extract_columns(df, "Hops")
    elif type == "carbon_error":
        df = extract_columns(df, "Error Carbon Val")
    else:
        print("Invalid type")
        exit(1)

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