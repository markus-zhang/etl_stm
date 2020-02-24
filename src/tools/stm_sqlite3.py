import sqlite3
import logging
import os
import json
from functools import wraps

# dirname = os.path.dirname(__file__)
# conn_string = os.path.join(dirname, '../../db/stm')

# Decorator for executors
def sqlite3_connector(conn_str):
    def sqlite3_decorator(func):
        # @wraps(fun)
        def with_connection_(*args, **kwargs):
            conn = sqlite3.connect(conn_str)
            try:
                dec_func = func(conn, *args, **kwargs)
            except Exception:
                conn.rollback()
                logging.error("Cannot connect to SQLite3 DB: " + conn_str)
                raise
            else:
                conn.commit()
            finally:
                conn.close()

            return dec_func
        return with_connection_
    return sqlite3_decorator

def add_timestamp_dict(d: dict, ts_key: str, ts_value: int):
    try:
        d[ts_key] = ts_value
    except ValueError:
        print(f'{__name__} error: Cannot add the following key-value: {ts_key}: {ts_value}')

# Convert dictionary values to tuple
# We can then insert tuples into sqlite3 database
def dict_value_to_tuple(d: dict)->tuple:
    return tuple(d.values())

if __name__ == '__main__':
    d: dict = json.loads(
        """{
            "ucmu_blue": "",
            "ucmu_red": "",
            "mip_green": "",
            "mip_orange": "",
            "mip_blue": "",
            "mip_yellow": "",
            "exists_mip": true,
            "all_lines": null,
            "query_time": 1582485166
        }"""
    )
    print(dict_value_to_tuple(d))