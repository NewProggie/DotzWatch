# Copyright (c) 2024, Kai Wolf - SW Consulting. All rights reserved.
# For the licensing terms see LICENSE file in the root directory. For the
# list of contributors see the AUTHORS file in the same directory.

from hashlib import md5
from config import *
from requests import get, post


def get_sid():
    sid_file = get_sid_file()
    try:
        with open(sid_file, 'r') as infile:
            sid = infile.read().strip()
    except FileNotFoundError:
        sid = kInvalidSid

    if sid != kInvalidSid:
        return sid

    login_sid_url = get_login_sid_url()
    login_check = get(f"{login_sid_url}?sid={sid}", verify=False)
    if kInvalidSid in login_check.text:
        challenge_response = get(f"{login_sid_url}", verify=False)
        challenge = challenge_response.text.split("<Challenge>")[1].split("</Challenge>")[0]
        user, passw = get_user_credentials()
        response = f"{challenge}-{md5((challenge + '-' + passw).encode('utf-16le')).hexdigest()}"
        login_response = post(
            f"{login_sid_url}", data={
            "response": response,
            "username": user
            }, verify=False
        )
        sid = login_response.text.split("<SID>")[1].split("</SID>")[0]
        with open(sid_file, 'w') as outfile:
            outfile.write(sid)
    return sid
