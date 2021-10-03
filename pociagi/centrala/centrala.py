from typing import Any
from celery.canvas import signature
from time import strftime
from celery import Celery
from celery.utils.log import get_task_logger
from requests.api import get, post

celery = Celery(__name__, broker="redis://redis")
logger = get_task_logger(__name__)


def senddata(postget, data: dict[str, Any], id: int):
    logger.debug(data, id)
    resp = postget("http://droznik-api:1100/endpoint/" + str(id), json=data)
    if resp.ok:
        logger.info("Droznik acknowledged the message.")
        return resp.json()
    else:
        logger.error(
            'Droznik didn\'t send an "ok" message. \
            Received this instead: '
            + str(resp.ok)
        )


@celery.task
def openbarrier(data):
    newdata = {"centrala": {"open": True}}
    senddata(post, newdata, data["stationid"])


def handlepociag(data) -> None:
    logger.debug("RESPONSE 1: " + str(data) + " of type " + str(type(data)))

    if "stationid" in data.keys():
        newdata = {"centrala": ["open"]}
        resp = senddata(get, newdata, data["stationid"])

        if isinstance(resp, dict):
            logger.warning(
                "Droznik didn't respond correctly. \
                assuming barrier is open."
            )
            resp = {str(data["stationid"]): {"open": True}}
        logger.info("RESPONSE 2: " + str(resp))
        if resp[str(data["stationid"])]["open"]:
            newdata = {"centrala": {"open": False}}
            resp = senddata(post, newdata, data["stationid"])
            logger.debug("RESPONSE 3: " + str(resp))
            if resp != {} and resp != "null":
                logger.error(
                    "ERROR. DROZNIK DIDN'T RESPOND \
                    CORRECTLY TO CLOSE COMMAND. ALERT CIVILIANS."
                )

        else:
            logger.warning("Anomaly: droznik already closed.")
        signature("centrala.openbarrier").apply_async(
            kwargs={"data": data}, queue="centrala", countdown=10
        )

    if "speed" in data.keys():
        spd = data["speed"]
        if spd < 40:
            f = open("/logs/slow.log", "a+")
            logger.info("Logging slow train speed.")
        elif spd < 140:
            f = open("/logs/normal.log", "a+")
            logger.info("Logging normal train speed.")
        elif spd < 180:
            f = open("/logs/fast.log", "a+")
            logger.info("Logging fast train speed.")
        else:
            logger.error("Anomaly: Pociag speed out of range.")
            return
        f.write(strftime("%Y-%m-%d %H:%M:%S : ") + str(spd) + " km/h\n")
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
