#!/usr/bin/env python3
#
# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from config import get_env
from docsis_parser import get_docsis_info
from fritzconn_parser import get_conn_info
from netspeed_parser import get_netspeed_info

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
        point.tag("channel", record.pop("channel"))
        for k, v in record.items():
            point.field(k, v)
        write_api.write(bucket="docsis", org=kOrg, record=point)

    # write FritzBox status
    for info in get_conn_info():
        point = Point("fritzbox")
        for k, v in info.items():
            point.field(k, v)
        write_api.write(bucket="fritzbox", org=kOrg, record=point)

    # write netspeed benchmark
    for info in get_netspeed_info():
        point = Point("netspeed")
        for k, v in info.items():
            point.field(k, v)
        write_api.write(bucket="netspeed", org=kOrg, record=point)

    client.close()

if __name__ == "__main__":
    main()
