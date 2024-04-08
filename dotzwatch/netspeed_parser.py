# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from config import get_data_url, get_data_payload
from fritz_login import get_sid
from json import loads as jloads
from numpy import percentile
from requests import post
import numpy as np


def fetch_netspeed_info():
    sid = get_sid()
    url = get_data_url()
    conn = post(url, get_data_payload("netMoni", sid), verify=False)
    return jloads(conn.text)


def parse_netspeed_info(info):
    output_data = []

    ds_bps_curr = info["data"]["sync_groups"][0]["ds_bps_curr"]
    us_default_bps_curr = info["data"]["sync_groups"][0]["us_realtime_bps_curr"]
    ds_ninety_fifth_percentile = percentile(ds_bps_curr, 95) / 8 / (2**20)
    us_ninety_fifth_percentile = percentile(us_default_bps_curr, 95) / 8 / (2**20)
    output_data.append(
        {
        "downspeed_mb": ds_ninety_fifth_percentile,
        "upspeed_mb": us_ninety_fifth_percentile
        }
    )

    return output_data


def get_netspeed_info():
    return parse_netspeed_info(fetch_netspeed_info)
