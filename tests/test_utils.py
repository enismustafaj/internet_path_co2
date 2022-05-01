import pytest
import sys
import os
import utils

sys.path.insert(1, os.path.join(sys.path[0], ".."))


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

        q = d / "ips2.csv"
        q.write_text("ip,country_code\n")
        with open(q, "r") as file:
            assert utils.check_header(file)

    def test_read_csv_file(self, tmp_path):
        d = tmp_path / "sub"
        d.mkdir()
        p = d / "ips.csv"
        p.write_text("ip,country_code\n")
        assert utils.read_csv_file(p) == []

    def test_create_res_dir(self, tmp_path):
        d = tmp_path / "sub"
        utils.create_res_dir(d)
        assert d.exists()

    def test_parse_output(self):
        assert utils.parse_output("") == []
        ip_addresses = ["111.123.123.13", "112.112.11.2"]
        assert len(utils.parse_output(" ".join(ip_addresses))) > 0
