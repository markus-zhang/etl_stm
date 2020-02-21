import requests as rq
from lxml import html
from response import get_response_status
from datetime import datetime as dt
from stm_sqlite3 import sqlite3_connector

def get_bus_dir(busno: int)->dict:
    """
        Because we do not know the direction (East, West / North South)
        We need to test one from each
    """
    # Should push these kinds of checks to app level
    if busno < 0:
        raise ValueError(f'{__name__}: Bus line number must be positive')
    
    url = f'https://m.stm.info/en/schedules/bus/{busno}/stops?direction='

    rp: dict = {}
    for dir in ['East', 'North']:        
        rp[dir] = get_response_status(url + dir, False)

    if rp:
        return rp
    else:
        raise ValueError(f'Failed to obtain response in {__name__}')

# TODO: See the next todo, needs to change the schema info
@sqlite3_connector
def dump_stop_info(dbconn, stoplist: list):
    cursor = dbconn.cursor()
    for s in stoplist:
        cursor.execute('INSERT INTO stm_stops_staging' + ' (bus_no, stop_seq, stop_content, query_timestamp) VALUES (?,?,?,?);', s)


def get_bus_stops(busno: int):
    """
        I need to generate the following tuple for staging table stm_bus_stops:
        bus_no:     51
        stop_seq:   1
        stop_name:  Gare Montréal-Ouest (Elmhurst/Sherbrooke)
        stop_id:    (50110)

        Both stop_name and stop_id are TEXT and should be transformed in later stages
    """

    status: dict = get_bus_dir(busno)
    dir: list = []

    if status['East'] == 200:
        dir.append('East')
        dir.append('West')

    if status['North'] == 200:
        dir.append('North')
        dir.append('South')

    # TODO: We need to modify the schema of stm_stops_staging
    # TODO: Add one column for direction (East/West/North/South)
    # TODO: And definitely change the code below
    for d in dir:
        with rq.get(
            f'https://m.stm.info/en/schedules/bus/{busno}/stops?direction={d}',
            verify=False
        ) as r:
            rawhtml = r.text
            newhtml = rawhtml.replace('\n\t\t', '')
            # newhtml = rawhtml

            tree = html.fromstring(newhtml)

            # firstnodelist = tree.xpath('//a[@class="stops-list-item stops-list-item-first"]')
            # firstnode = firstnodelist[0]
            # firststopnode = firstnode.xpath('//span[@class="stops-list-item-desc"]')

            firststop = tree.xpath('//a[@class="stops-list-item stops-list-item-first"]')
            firststopname = firststop[0].xpath('//span[@class="stops-list-item-desc"]')
            firststopid = firststopname[0].xpath('//span[@class="stops-list-item-id"]')

            reststops = tree.xpath('//a[@class="stops-list-item "]')

            stop_list = []

            # Get query time
            queryepoch = int(dt.now().timestamp())
            # Generate tuple for first stop
            stop_seq = 1
            # print(firststopname[0].text_content())
            stop_tuple = (busno, stop_seq, firststopname[0].text_content().strip(), queryepoch)
            stop_list.append(stop_tuple)
            # print(stop_tuple)
            # print(firststopname[0].text.strip())    # This only shows the text inside of this span and will exclude the children
            # print(firststopid[0].text.strip())
            # print(firststop[0].attrib['href'])      # Use attrib property to grab the attributes (e.g. href) INSIDE of <span ...>
            for stop in reststops:
                stop_seq += 1
                stop_tuple = (busno, stop_seq, stop.text_content().strip(), queryepoch)
                # print(stop.text_content())
                stop_list.append(stop_tuple)

            dump_stop_info(stop_list)
                

if __name__ == "__main__":
    rq.packages.urllib3.disable_warnings() 
    get_bus_stops(51)
