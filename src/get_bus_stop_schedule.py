import requests as rq
from lxml import html
from response import get_response_status
from datetime import datetime as dt
from stm_sqlite3 import sqlite3_connector


def get_bus_stop_schedule(busno: int, stop: int, limit: int = 5):
    pass