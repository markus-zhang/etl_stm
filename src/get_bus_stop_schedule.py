import requests as rq
import os
import sys
from lxml import html
from response import get_response_status
from datetime import datetime as dt
from tools.stm_sqlite3 import sqlite3_connector
from get_bus_stops import get_bus_stops


@sqlite3_connector(f'{os.path.join(os.path.dirname(__file__), "stm")}')
def get_stop_direction(dbconn, busno: int, stopno: int, hotscrape=False)-> str:
    """
        Helper function for get_bus_stop_schedule;
        Extract direction information from the database
        based on busno and stopno
        Cursor returns a list containing one tuple (int_1, int_2, str)

        int_1: same as busno if found in database
        int_2: same as stopno if found in database
        str: same as direction if found

        Because this function is ALWAYS called after the user accesses
        a bus no, so we can safely conclude that the busno exists and
        only the stopno is missing 
    """
    cursor = dbconn.cursor()
    cursor.execute(
        f'  SELECT bus_no, stop_no, direction \
            FROM stm_stops \
            WHERE bus_no = {busno} AND stop_no = {stopno}'
    )

    rv: list = cursor.fetchall()
    if len(rv) == 0:
        # stopno is missing
        # try to hot-scrape the information, push to db, and rerun the query
        # However stop the process if we already hot-scraped
        if hotscrape is True:
            # TODO: log and display Critical Error
            print(f'Route {busno} has no stop {stopno} in either direction')
            sys.exit()
        else:
            print(f'Hot scraping route {busno}...')
            get_bus_stops(busno)
            get_stop_direction(busno, stopno, True)
    else:
        print(rv[0])
        pass



def get_bus_stop_schedule(busno: int, stopno: int, limit: int = 5):
    # https://m.stm.info/en/schedules/bus/51/stops/50110/arrivals?limit=10&direction=East
    """
        We will first try to pull the direction from the database using:
        SELECT 
            direction 
        FROM 
            -- The staging table doesn't work in this case
            stm_stops 
        WHERE 
            bus_no = busno
            AND stop_no = stop

        If it returns
    """
    pass

if __name__ == '__main__':
    get_stop_direction(79, 51962)