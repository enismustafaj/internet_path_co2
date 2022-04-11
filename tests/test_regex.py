import re
import pytest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import constants


class TestRegex:
    def test_ip_v4(self):
        ip = "111.111.111.111"
        assert re.match(constants.IP_V4_REGEX, ip)

        ip = "111.111"
        assert not re.match(constants.IP_V4_REGEX, ip)

        ip = "some random text \n [123.123.123.123]"
        assert len(re.findall(constants.IP_V4_REGEX, ip)) > 0

    def test_ip_v6(self):
        pass
