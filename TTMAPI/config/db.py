import mongoengine
from dotenv import dotenv_values


config = dotenv_values("settings.env")


def getDB():
    client = mongoengine.connect(
        host=config["CLIENT_URL"])
    db = client["test"]

    return db
