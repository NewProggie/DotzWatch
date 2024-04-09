# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from config import get_data_url, get_data_payload
from json import loads as jloads
from fritz_login import get_sid
from requests import post


def fetch_docsis_info():
    sid = get_sid()
    url = get_data_url()
    docsis = post(url, get_data_payload("docInfo", sid), verify=False)
    return jloads(docsis.text)


def parse_docsis_info(docsis_data):
    output_data = []

    # Determine the modulation key based on the presence of "type" or "modulation" in the JSON
    modulation_key = "modulation" if docsis_data["data"]["channelUs"]["docsis30"][
        0].get("type") is None else "type"

    # Get number of upstream and downstream channels
    channel_us_cnt = len(docsis_data["data"]["channelUs"]["docsis30"])
    channel_ds_cnt = len(docsis_data["data"]["channelDs"]["docsis30"])

    # Process upstream channels
    for i in range(channel_us_cnt):
        channel = docsis_data["data"]["channelUs"]["docsis30"][i]
        output_data.append(
            {
            "mode": "up",
            "channel": channel['channel'],
            "channelID": channel['channelID'],
            "Modulation": float(channel[modulation_key].replace('QAM', '')),
            "PowerLevel": float(channel['powerLevel']),
            "Frequenz": float(channel['frequency']),
            }
        )

    # Process downstream channels
    for i in range(channel_ds_cnt):
        channel = docsis_data["data"]["channelDs"]["docsis30"][i]
        output_data.append(
            {
            "mode": "down",
            "channel": channel['channel'],
            "channelID": channel['channelID'],
            "Modulation": float(channel[modulation_key].replace('QAM', '')),
            "PowerLevel": float(channel['powerLevel']),
            "Frequenz": float(channel['frequency']),
            "Latenz": float(channel['latency']),
            "korrFehler": float(channel['corrErrors']),
            "Fehler": float(channel['nonCorrErrors'])
            }
        )

    return output_data


def get_docsis_info():
    return parse_docsis_info(fetch_docsis_info())
