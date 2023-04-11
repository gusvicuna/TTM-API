import pymongo
from dotenv import dotenv_values


config = dotenv_values("settings.env")


def getDB():
    client = pymongo.MongoClient(
        config["CLIENT_URL"])
    db = client.test

    return db
