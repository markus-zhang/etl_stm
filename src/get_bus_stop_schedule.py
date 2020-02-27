import requests as rq
from lxml import html
from response import get_response_status
from datetime import datetime as dt
from stm_sqlite3 import sqlite3_connector


def get_bus_stop_schedule(busno: int, stop: int, limit: int = 5):
    # https://m.stm.info/en/schedules/bus/51/stops/50110/arrivals?limit=10&direction=East
    """
        Since get_bus_stop_schedule is always called after get_bus_stop,
        we can safely pull the direction from the database
    """