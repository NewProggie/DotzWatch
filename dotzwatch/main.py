#!/usr/bin/env python3
#
# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from config import get_env
from dotzwatch.docsis_parser import get_docsis_info

kInfluxUrl = "http://127.0.0.1:8086"
kInfluxToken = get_env("INFLUX_TOKEN")
kOrg = "kwc"


def main():
    client = InfluxDBClient(url=kInfluxUrl, token=kInfluxToken, org=kOrg)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # write DOCSIS info
    for record in get_docsis_info():
        point = Point("docsis")
        point.tag("mode", record.pop("mode"))
        for k, v in record.items():
            point.field(k, v)
        write_api.write(bucket="docsis", org=kOrg, record=point)
    client.close()


if __name__ == "__main__":
    main()
