from time import time
from celery import Celery
from celery.canvas import signature
from flask import Flask
from pociagi.droznik.stationgenerator import generatestation
import pociagi.droznik.models as models
import logging

app = Flask(__name__)
celery = Celery(__name__,broker="redis://redis")

@celery.task
def messagehandler(data : dict[str, dict]): # -> int | dict
    if "centrala" in data.keys():
        data=data["centrala"]
        id = list(data.keys())[0]
        if type(data[id])==type([]):
            open=True #### get state of the barrier
            newdata = { id: { "open": open } }
            return newdata
        elif type(data[id])==type({}): # send back information
            # pseudocode: db.stacja.open = data[id]["open"]
            return 0

def getstations():
    for i in range(20):
        station = generatestation()
        dbstation = models.Stacja(id=i,name=station)
        dbbarrier = models.Szlaban(id=i,open=True,last=time(),station=dbstation)
        models.db.session.add(dbstation)
        models.db.session.add(dbbarrier)
    models.db.session.commit()
    print(models.db.session.query(models.Stacja).all())

if __name__=="__main__":
    app.run(host="droznik-api",port=1100)
    celery.start()
    models.db.create_all()