import pytest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import export
import pandas as pd


class TestExport:
    def test_create_json_output(self):
        empty_content = {}
        runs = {}
        assert export.create_json_output(runs, empty_content) == {}

        content = {
            "1": {
                "hops": ["1", "2", "3"],
                "carbon_intensities": [1, 2, 3],
                "countries": ["DE", "DE", "DE"],
            },
        }
        runs = {}
        runs = export.create_json_output(runs, content)
        assert runs == {"1": [3, 6, 0, 0]}

    def test_create_csv_output(self, tmp_path):
        df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=["A", "B", "C"])
        output = tmp_path / "test.csv"
        export.create_csv_output(df, output)
        assert output.exists()

    def test_extract_columns(self):
        df = pd.DataFrame(
            [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9],
                [10, 11, 12],
                [13, 14, 15],
            ],
            columns=["A", "B", "C"],
        )
        cols = export.extract_columns(df, "B")
        assert cols.columns.tolist() == ["A", "B"]
