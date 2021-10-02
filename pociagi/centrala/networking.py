from typing import Any
from requests import post, get, Response
import logging

def senddata(postget: str, data: dict[str, Any], host: str, params: str = "" ):
    try:
        resp = postget("http://"+host+"/endpoint/"+params, json=data)
        if resp.ok:
            logging.info("Host "+host+" acknowledged the message.")
            return resp.json
        else:
            logging.error("Host "+host+" didn't send an \"ok\" message.")
    except:
        logging.error("Can't establish connection to host "+host+".")