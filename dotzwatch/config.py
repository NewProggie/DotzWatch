# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from os import environ

kInvalidSid = "0000000000000000"


def get_env(var_name):
    """Attempts to get an environment variable"""
    try:
        return environ[var_name]
    except KeyError:
        raise EnvironmentError(f"Required environment variable '{var_name}' not set.")


def get_user_credentials():
    username = get_env("FRITZ_USER")
    password = get_env("FRITZ_PASS")
    return username, password


def get_login_sid_url():
    fritzbox = get_env("FRITZBOX")
    port = get_env("FRITZ_PORT")
    return "https://{fritzbox}:{port}/login_sid.lua"


def get_data_url():
    fritzbox = get_env("FRITZBOX")
    port = get_env("FRITZ_PORT")
    return f"https://{fritzbox}:{port}/data.lua"


def get_data_payload(page, sid):
    return {"xhr": 1, "sid": sid, "lang": "de", "page": page, "xhrId": "all", "no_sidrenew": ""}


def get_sid_file():
    fritzbox = get_env("FRITZBOX")
    return f"/tmp/{fritzbox}.sid"
