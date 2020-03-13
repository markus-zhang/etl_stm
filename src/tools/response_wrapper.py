"""
    A thin wrapper for the respons library
"""
import logging
from datetime import datetime as dt
import requests as rq
from urllib3.exceptions import InsecureRequestWarning

# TODO: Add support for logging
def get_response(url: str, verifyssl: bool= False, hd: dict={}, payload: dict={}, log: str='')-> tuple:
    """
        Functionality: 
            Returns (status, text) for a request;
            Produce logs if log is not empty

        Params:
            url:        The remote address
            verifyssl:  Default as False for STM
            log:        log file name
    """
    if verifyssl is False:
        # Suppress the warning if ignore SSL:
        # https://stackoverflow.com/questions/15445981/how-do-i-disable-the-security-certificate-check-in-python-requests
        rq.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    with rq.Session() as s:
        try:
            r= s.get(url, verify=verifyssl, headers=hd, params=payload)
            # if len(r.text) <= 0:
            # raise ValueError(f'{__name__} error: Response text has length 0')

            return (r.status_code, r.text)
        except (
            rq.exceptions.ConnectionError,
            rq.exceptions.HTTPError,
            rq.exceptions.ConnectTimeout,
            rq.exceptions.Timeout
        ) as e:
            # TODO: log Critical Error
            return (-1, "Network Error")