# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from json import load as jload
from unittest import TestCase
from pathlib import Path
from dotzwatch.fritzconn_parser import parse_conn_info


class TestFritzConnParser(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        test_path = Path(__file__).parent.parent / 'assets' / 'test' / 'overview.json'
        with open(test_path) as infile:
            cls.fritzconn_data = jload(infile)

    def test_parse_conn_info(self):
        result = parse_conn_info(self.fritzconn_data)
        self.assertTrue(result)
        for info in result:
            self.assertTrue("uptime" in info.keys())
            self.assertTrue("is_connected" in info.keys())
            self.assertTrue("ip_address" in info.keys())
