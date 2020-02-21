"""
    Scripts starting with "pull_" pulls data from database instead of STM
"""

from stm_sqlite3 import sqlite3_connector
import sqlite3 as sq

@sqlite3_connector
def pull_bus_direction(conn, busno: int):
    cursor: sq.Cursor = conn.cursor()
    cursor.execute(
        f'SELECT * FROM stm_stops_staging WHERE bus_no = {busno}'
    )

    print(cursor.fetchall())


if __name__ == '__main__':
    pull_bus_direction(51)