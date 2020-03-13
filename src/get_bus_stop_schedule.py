import requests as rq
import os
import sys
from lxml import html
from response import get_response_status
from datetime import datetime as dt
from tools.stm_sqlite3 import sqlite3_connector
from get_bus_stops import get_bus_stops
from tools.response_wrapper import get_response

# TODO: In the future we should rebuild this module
# Instead of querying the database each time, the app should:
# 1. Query the database and dump all bus and stop info into a data structure
# 2. This module will only hit the scraper if the requested info is not in it
# 3. The scraper will scrape STM and in turn update the database
# 4. And it will re-dump the whole info again in (or update part of) the dictionary

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

        Return a tuple like (78, 51962, 'West') if records are found
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
        return rv[0][2]



def get_bus_stop_schedule(busno: int, stopno: int, limit: int = 5):
    # https://m.stm.info/en/schedules/bus/51/stops/50110/arrivals?limit=10&direction=East
    """
        We will first try to pull the direction from the database using:
        get_stop_direction()

        If it returns a tuple like (78, 51962, 'West') then everything is fine
    """
    direction: str = get_stop_direction(busno, stopno, False)

    url = f'https://m.stm.info/en/schedules/bus/{busno}/stops/{stopno}/arrivals?limit={limit}&direction={direction}'
    payload = {
        'limit': str(limit),
        'direction': direction
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'DNT': '1',
        'Host': 'm.stm.info',
        'If-None-Match': '"5dd514-4bb44d6fe21f"',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Mobile Safari/537.36',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    rawhtml = get_response(url, False, headers, payload)[1]

if __name__ == '__main__':
    get_bus_stop_schedule(78, 51962)