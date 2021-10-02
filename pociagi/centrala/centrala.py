from celery.canvas import signature
from time import strftime
from flask import Flask
from celery import Celery
from celery.result import allow_join_result
from celery.utils.log import get_task_logger

app = Flask(__name__)
celery = Celery(app.import_name,broker="redis://redis", backend="cache+memory://")
logger = get_task_logger(app.import_name)


@celery.task
def openbarrier(data):
    logger.error(data)
    newdata = { "centrala" : { data["stationid"] : { "open" : True } } }
    signature("pociagi.droznik.droznik.messagehandler").apply_async(kwargs={"data":newdata}, queue="droznik")

def handlepociag(data) -> None:
    logger.debug("Received data: " + str(data) + " of type "+str( type(data) ) )

    if "stationid" in data.keys():
        newdata = { "centrala" : { data["stationid"] : ["open"] } }
        res = signature("pociagi.droznik.droznik.messagehandler").apply_async(kwargs={"data":newdata}, queue="droznik", expires=10)
        try:
            resp = res.get(disable_sync_subtasks=False, timeout=0.1)
        except:
            resp=False
        res.forget()
        logger.debug(str("Response: "+str(resp)))
        if type(resp)!=type({}):
            logger.warning("Droznik didn't respond correctly. assuming barrier is open.")
            resp = { data["stationid"]: { "open": True }}
        if resp[data["stationid"]]["open"]:
            newdata = { "centrala": { data["stationid"] : { "open" : False } } }
            res = signature("pociagi.droznik.droznik.messagehandler").apply_async(kwargs={"data":newdata}, queue="droznik", expires=10)
            try:
                resp=res.get(disable_sync_subtasks=False, timeout=0.1)
            except:
                logger.error("ERROR. DROZNIK DIDN'T RESPOND TO CLOSE COMMAND. ALERT CIVILIANS.")
        else:
            logger.warning("Anomaly: droznik already closed.")
        signature("centrala.openbarrier").apply_async(kwargs={"data":data}, queue="centrala", countdown=10)
            
    if "speed" in data.keys():
        spd = data["speed"]
        if spd<40:
            f = open("/logs/slow.log","a+")
            logger.info("Logging slow train speed.")
        elif spd<140:
            f = open("/logs/normal.log","a+")
            logger.info("Logging normal train speed.")
        elif spd<180:
            f = open("/logs/fast.log","a+")
            logger.info("Logging fast train speed.")
        else:
            logger.error("Anomaly: Pociag speed out of range.")
            return
        f.write(strftime("%Y-%m-%d %H:%M:%S : ")+str(spd)+" km/h\n")
        f.close()

responses: dict = {
    "pociag": handlepociag,
}

@celery.task
def messagehandler(data: dict[str, dict]):
    for r in data.keys():
        if r in responses.keys():
            responses[r](data[r])
    return 0

if __name__ == "__main__":
    celery.start()
    app.run(host="centrala-api",port=1200)