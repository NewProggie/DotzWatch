# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from json import load as jload
from unittest import TestCase
from pathlib import Path
from dotzwatch.netspeed_parser import parse_netspeed_info


class TestNetSpeedParser(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        test_path = Path(__file__).parent.parent / 'assets' / 'test' / 'netMoni.json'
        with open(test_path) as infile:
            cls.netspeed_data = jload(infile)

    def test_parse_conn_info(self):
        result = parse_netspeed_info(self.netspeed_data)
        self.assertTrue(result)
        for record in result:
            self.assertTrue("downspeed_mb" in record.keys())
            self.assertTrue("upspeed_mb" in record.keys())
