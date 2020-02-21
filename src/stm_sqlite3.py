import sqlite3
import logging
import os

dirname = os.path.dirname(__file__)
conn_string = os.path.join(dirname, '../db/stm')

# Decorator for executors
def sqlite3_connector(func):
    def with_connection_(*args, **kwargs):
        conn = sqlite3.connect(conn_string)
        try:
            dec_func = func(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            logging.error("Cannot connect to SQLite3 DB: " + conn_string)
            raise
        else:
            conn.commit()
        finally:
            conn.close()

        return dec_func
    return with_connection_