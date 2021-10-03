from random import randrange
from celery.canvas import signature
from config import POCIAG_DELAY, POCIAG_DELAY_2, POCIAG_MAX_SPEED
from flask import Flask
from celery import Celery
import logging

celery = Celery(__name__,broker="redis://redis")

stations={}

@celery.task
def getstations(data: dict[int,str]):
    global stations
    for i in range(len(list(data.keys()))):
        stations[i]=data[str(i)]

@celery.task
def sendspeeddata() -> None:
    data = { "pociag" : { "speed" : float(randrange(0,POCIAG_MAX_SPEED*10))/10 } }
    signature("centrala.messagehandler").apply_async(kwargs={"data":data}, queue="centrala")

@celery.task
def sendstationdata() -> None:
    try:
        chosen=randrange(len(list(stations.keys())))
    except ValueError:
        logging.error("Didn't receive stations. Please reset droznik-api.")
        return
    data = { "pociag" : { "stationid" : chosen } }
    logging.info("Train incoming to station "+stations[chosen])
    signature("centrala.messagehandler").apply_async(kwargs={"data":data}, queue="centrala")

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(POCIAG_DELAY, signature("pociag.sendspeeddata", args=(), options={"queue": "pociag"}))
    sender.add_periodic_task(POCIAG_DELAY_2, signature("pociag.sendstationdata", args=(), options={"queue": "pociag"}))
