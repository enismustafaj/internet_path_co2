import pytest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import export


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
