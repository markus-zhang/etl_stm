import requests as rq
import json
import sqlite3
from stm_sqlite3 import sqlite3_connector
from datetime import datetime as dt

def get_response(url: str, verifyssl: bool = False) -> str:
    with rq.get(url, verify=verifyssl) as r:
    
        if len(r.text) <= 0:
            raise ValueError(f'{__name__} error: Response text has length 0')

    return r.text


def str2dict(s: str) -> dict:
    return json.loads(s)

def add_timestamp_dict(d: dict, ts_key: str, ts_value: int):
    try:
        d[ts_key] = ts_value
    except ValueError:
        print(f'{__name__} error: Cannot add the following key-value: {ts_key}: {ts_value}')

def printdict(d: dict, sortkey: bool = True, ind: int = 4):
    print(json.dumps(d, sort_keys=sortkey, indent=ind))


@sqlite3_connector
def dump_stm_stream(dbconn: sqlite3.connect, ):
    pass


if __name__ == "__main__":
    """
        1 - Scape the current status of STM services as a Python dict
        2 - Insert current time into said dict as epoch int
        3 - Insert dict into splite3 db as tuple
    """

    queryepoch = int(dt.now().timestamp())
    rawdict: dict = str2dict(get_response("https://m.stm.info/en/home.json", False))
    add_timestamp_dict(rawdict, "query_time", queryepoch)

    printdict(rawdict, False, 4)

    schema = [
        "ucmu_blue", "ucmu_red",
        "mip_green", "mip_blue", "mip_yellow",
        "exists_mip",
        "all_lines",
        "query_epoch"
    ]

    db = "..\\db\\stm"
    table = "stm_status_staging"

    



# r: rq.Response = rq.get('https://m.stm.info/en/home.json', verify=False)

# d: dict = json.loads(r.text)

# print(json.dumps(d, sort_keys=True, indent=4))