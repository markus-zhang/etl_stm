import sqlite3
import logging


# Decorator for executors
def sqlite3_connector(func, conn_string: str):
    def with_connection_(*args, **kwargs):
        conn = sqlite3.connect(conn_string)
        try:
            dec_func = func(conn, *args, **kwargs)
        except Exception:
            conn.rollback()
            logging.error("SQLite3 Database Connection Error")
            raise
        else:
            conn.commit()
        finally:
            conn.close()

        return dec_func
    return with_connection_