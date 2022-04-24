import sys
import pandas as pd
import os
import json

import matplotlib.pyplot as plt


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


def export_data(source, output_file_name):
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

    fig, ax = plt.subplots(1, 1, figsize=(20, 15))

    fig.patch.set_visible(False)
    ax.axis("off")
    ax.axis("tight")

    df["Destination"] = df.index.to_numpy().flatten()

    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc="center",
    )
    fig.tight_layout()
    fig.savefig(output_file_name)


if __name__ == "__main__":
    export_data(sys.argv[1], sys.argv[2])
