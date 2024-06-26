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
from speedtest import Speedtest

kInfluxUrl = "http://127.0.0.1:8086"
kInfluxToken = get_env("INFLUX_TOKEN")
kOrg = "kwc"


def main():
    client = InfluxDBClient(url=kInfluxUrl, token=kInfluxToken, org=kOrg)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    s = Speedtest()
    s.get_best_server()

    s.download()
    s.upload()

    # write speedtest benchmark results
    results = s.results.dict()
    point = Point("netspeed")
    point.field("download",  results['download'] / 8 / (2**20))
    point.field("upload",  results['upload'] / 8 / (2**20))
    write_api.write(bucket="netspeed", org=kOrg, record=point)
    client.close()

if __name__ == "__main__":
    main()
