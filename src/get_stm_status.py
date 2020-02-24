import requests as rq
import json
import os
import sys
# import sqlite3
from tools.stm_sqlite3 import *
from datetime import datetime as dt
from tools.response_wrapper import *

# def get_response(url: str, verifyssl: bool = False) -> str:
#     with rq.get(url, verify=verifyssl) as r:
    
#         if len(r.text) <= 0:
#             raise ValueError(f'{__name__} error: Response text has length 0')

#     return r.text


def str2dict(s: str) -> dict:
    return json.loads(s)

def add_timestamp_dict(d: dict, ts_key: str, ts_value: int):
    try:
        d[ts_key] = ts_value
    except ValueError:
        print(f'{__name__} error: Cannot add the following key-value: {ts_key}: {ts_value}')

def printdict(d: dict, sortkey: bool = True, ind: int = 4):
    print(json.dumps(d, sort_keys=sortkey, indent=ind))

# TODO: See if we can pass the argument to sqlite3_connector instead of hard-code
@sqlite3_connector(f'{os.path.join(os.path.dirname(__file__), "../db/stm")}')
def dump_stm_status(dbconn: sqlite3.connect, status_tuple: tuple):
    """
        Dump the tuple into database
    """
    cursor = dbconn.cursor()
    schema: str = """(
        ucmu_blue, ucmu_red,
        mip_green, mip_blue, mip_yellow,
        exists_mip,
        all_lines,
        query_epoch
    )"""
    value: str = '(' + '? ' * len(status_tuple) + ')'
    print(f'INSERT INTO stm_status_staging {schema} VALUES {value};', status_tuple)


def get_stm_status():
    """
        1 - Scape the current status of STM services as a Python dict
        2 - Insert current time into said dict as epoch int
        3 - Insert dict into splite3 db as tuple
    """
    queryepoch = int(dt.now().timestamp())
    status, text = get_response('https://m.stm.info/en/home.json', False)

    if status != 200:
        # TODO: Log Critical Error and terminate program
        sys.exit()
    else:
        statusdict: dict = json.loads(text)
        add_timestamp_dict(statusdict, "query_time", queryepoch)
        statustuple: tuple = dict_value_to_tuple(statusdict)

        # Dump status to database
        dirname = os.path.dirname(__file__)
        conn_string = os.path.join(dirname, '../db/stm')

if __name__ == "__main__":
    """
        1 - Scape the current status of STM services as a Python dict
        2 - Insert current time into said dict as epoch int
        3 - Insert dict into splite3 db as tuple
    """

    # queryepoch = int(dt.now().timestamp())
    # rawdict: dict = str2dict(get_response("https://m.stm.info/en/home.json", False))
    # add_timestamp_dict(rawdict, "query_time", queryepoch)

    # printdict(rawdict, False, 4)

    # schema = [
    #     "ucmu_blue", "ucmu_red",
    #     "mip_green", "mip_blue", "mip_yellow",
    #     "exists_mip",
    #     "all_lines",
    #     "query_epoch"
    # ]

    # db = "..\\db\\stm"
    # table = "stm_status_staging"
    dirname = os.path.dirname(__file__)
    conn_string = os.path.join(dirname, '../db/stm')
    dump_stm_status((1,2,9))



# r: rq.Response = rq.get('https://m.stm.info/en/home.json', verify=False)

# d: dict = json.loads(r.text)

# print(json.dumps(d, sort_keys=True, indent=4))