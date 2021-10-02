from traceback import print_exc
from random import randrange
from celery.canvas import signature
from config import POCIAG_DELAY, POCIAG_MAX_SPEED
from flask import Flask
from celery import Celery
import logging

app = Flask(__name__)
celery = Celery(app.import_name,broker="redis://redis")

@celery.task
def sendspeeddata() -> None:
    data = { "pociag" : { "speed" : float(randrange(0,POCIAG_MAX_SPEED*10))/10 } }
    signature("centrala.messagehandler").apply_async(kwargs={"data":data}, queue="centrala")

@celery.task
def sendstationdata() -> None:
    data = { "pociag" : { "stationid" : 0 } } #############################
    signature("centrala.messagehandler").apply_async(kwargs={"data":data}, queue="centrala")

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    #sender.add_periodic_task(POCIAG_DELAY, signature("pociag.sendspeeddata", args=(), options={"queue": "pociag"}))
    sender.add_periodic_task(10.0, signature("pociag.sendstationdata", args=(), options={"queue": "pociag"}))

if __name__ == "__main__":
    app.run()
    celery.start()
