from time import time
from celery import Celery
from celery.canvas import signature
from flask import Flask, request, jsonify
from sqlalchemy.sql.functions import now
try:
    from pociagi.droznik.stationgenerator import generatestation
    import pociagi.droznik.models as models
except:
    from stationgenerator import generatestation
    import models
import logging

app = Flask(__name__)
celery = Celery(__name__,broker="redis://redis")

@app.route("/endpoint/<id>", methods=["GET","POST"])
def messagehandler(id): # -> int | dict
    data=request.json
    if "centrala" in data.keys():
        data=data["centrala"]
        logging.debug(data)
        if type(data)==type([]):
            if "open" in data:
                open = models.db.session.query(models.Szlaban).filter(models.Szlaban.id==id).first().open
                models.db.session.close()
                newdata = { id: { "open": open } }
                logging.debug("RETURNING DATA: "+str(newdata))
                return newdata, 200
        elif type(data)==type({}):
            logging.debug(data)
            barrier=models.db.session \
                    .query(models.Szlaban) \
                    .filter(models.Szlaban.id==id) \
                    .first()
            setattr(barrier, "open", data["open"] )
            setattr(barrier, "last", now())
            models.db.session.commit()
            models.db.session.close()
            logging.debug("RETURNING DATA: {}")
            return {}, 200
        else:
            return None, 400

def createstations():
    stations=[]
    for i in range(20):
        while 1:
            station = generatestation()
            if station not in stations:
                stations.append(station)
                break
    for station, i in zip(stations, range(20)):
        dbstation = models.Stacja(id=i,name=station)
        dbbarrier = models.Szlaban(id=i,open=True,last=now())#,station=dbstation)
        models.db.session.add(dbstation)
        models.db.session.add(dbbarrier)
    models.db.session.commit()
    ret = models.db.session.query(models.Stacja).all()
    models.db.session.close()
    return ret

def setupdb():
    models.db.drop_all()
    models.db.create_all()
    return createstations()

def sendstations(data: list[models.Stacja]):
    newdata={}
    for stacja in data:
        newdata[int(stacja.id)]=stacja.name # int() do usuniecia?
    signature("pociag.getstations").apply_async(args=(),kwargs={"data":newdata}, queue="pociag")

if __name__=="__main__":
    sendstations(setupdb())
    app.run(host="droznik-api",port=1100)