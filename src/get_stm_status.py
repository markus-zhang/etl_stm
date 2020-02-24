import requests as rq
import json
import os
import sys
import sqlite3
from tools.stm_sqlite3 import *
from datetime import datetime as dt
from tools.response_wrapper import *

# TODO: See if we can pass the argument to sqlite3_connector instead of hard-code
# @sqlite3_connector(f'{os.path.join(os.path.dirname(__file__), "../db/stm")}')
@sqlite3_connector(f'{os.path.join(os.path.dirname(__file__), "stm")}')
def dump_stm_status(dbconn: sqlite3.connect, status_tuple: tuple):
    """
        Dump the tuple into database
    """
    cursor = dbconn.cursor()
    schema: str = """(
        ucmu_blue, ucmu_red,
        mip_green, mip_orange, mip_blue, mip_yellow,
        exists_mip,
        all_lines,
        query_time
    )"""
    value: str = '(' + '?,' * (len(status_tuple)-1) + '?)'
    print(f'INSERT INTO stm_status_staging {schema} VALUES {value};')
    cursor.execute(f'INSERT INTO stm_status_staging {schema} VALUES {value};', status_tuple)


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
        # Remove None
        # if statusdict['all_lines'] is None:
        #     statusdict['all_lines'] = 'None'
        statustuple: tuple = dict_value_to_tuple(statusdict)

        # Dump status to database
        print(statustuple)
        dump_stm_status(statustuple)

if __name__ == "__main__":
    """
        1 - Scape the current status of STM services as a Python dict
        2 - Insert current time into said dict as epoch int
        3 - Insert dict into splite3 db as tuple
    """

    get_stm_status()
