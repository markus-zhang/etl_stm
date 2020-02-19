"""
    A thin wrapper of the requests library for this project
"""

import requests as rq

def get_response_status(url: str, veri=False):
    with rq.get(url, verify=veri) as r:
        return r.status_code