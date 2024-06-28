#
# Server management stuff
#
# Follow the REST API documentation
# https://tech.palworldgame.com/category/rest-api
#
# REMINDER: 8212 TCP must be enabled on your firewall!
#

import requests
from config import PALWORLD_SERVER_URL
from settings import PALWORLD_SECRET_AUTH


def invoke_pal_get_data(item: str) -> requests.request:
    url: str = PALWORLD_SERVER_URL + item

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': PALWORLD_SECRET_AUTH
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

def invoke_pal_save_world(item: str) -> requests.request:
    url: str = PALWORLD_SERVER_URL + item

    payload={}
    headers = {
        'Authorization': PALWORLD_SECRET_AUTH
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text
