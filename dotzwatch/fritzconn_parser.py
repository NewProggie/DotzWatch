# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from config import get_data_url, get_data_payload
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fritz_login import get_sid
from json import loads as jloads
from requests import post

def human_readable_uptime(since_timestamp):
    # Calculate the difference between now and the uptime timestamp
    uptime_start = datetime.fromtimestamp(since_timestamp)
    now = datetime.now()
    diff = relativedelta(now, uptime_start)

    # Build a list of the time components that are non-zero
    components = [
        f"{diff.years} years" if diff.years else "",
        f"{diff.months} months" if diff.months else "",
        f"{diff.days} days" if diff.days else "",
        f"{diff.hours} hours" if diff.hours else "",
        f"{diff.minutes} minutes" if diff.minutes else "",
    ]

    # Filter out empty strings and join the remaining components
    readable_uptime = ', '.join(filter(None, components))

    return readable_uptime or "Less than a minute"

def fetch_conn_info():
    sid = get_sid()
    url = get_data_url()
    conn = post(url, get_data_payload("overview", sid), verify=False)
    return jloads(conn.text)

def parse_conn_info(info):
    v4_connected = info["data"]["internet"]["connections"][0]["ipv4"]["connected"]
    v4_uptime = info["data"]["internet"]["connections"][0]["ipv4"]["since"]
    print(human_readable_uptime(v4_uptime))

    v6_connected = info["data"]["internet"]["connections"][0]["ipv6"]["connected"]
    v6_uptime = info["data"]["internet"]["connections"][0]["ipv6"]["since"]
    print(human_readable_uptime(v6_uptime))
    return info