import requests
from time import sleep
from config import POCIAG_DELAY

test = { "pociag" : {"speed" : 1, "station": "A"} }

if __name__=="__main__":
    while 1:
        try:
            res = requests.post("http://centrala-api:1200/centrala/endpoint", json=test)
            if res.ok:
                print(res.text)
            else:
                print("sent but failed")
        except:
            print("failed")
        sleep(POCIAG_DELAY)