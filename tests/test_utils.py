import pytest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import utils


class TestUtils:
    def test_csv_header(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "ips.csv"
        p.write_text("ip,country_code\n")
        with open(p, "r") as file:
            assert utils.check_header(file)

    def test_csv_header_fail(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "ips.csv"
        p.write_text('"111.111.111.111", "US"\n')
        with open(p, "r") as file:
            assert not utils.check_header(file)

    def test_read_filesites(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "ips.csv"
        p.write_text("ip,country_code\n")
        assert utils.read_filesites(p) == []
