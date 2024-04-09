# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from json import load as jload
from unittest import TestCase
from pathlib import Path
from dotzwatch.docsis_parser import parse_docsis_info


class TestDOCSISParser(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        test_path = Path(__file__).parent.parent / 'assets' / 'test' / 'docInfo.json'
        with open(test_path) as infile:
            cls.docsis_data = jload(infile)

    def test_parse_docsis_info(self):
        result = parse_docsis_info(self.docsis_data)
        self.assertTrue(result)
        for record in result:
            self.assertTrue("mode" in record.keys())
            self.assertTrue("channel" in record.keys())
            self.assertTrue("Modulation" in record.keys())
            self.assertTrue("PowerLevel" in record.keys())
            self.assertTrue("Frequenz" in record.keys())
            self.assertTrue(record["mode"] == "up" or record["mode"] == "down")
