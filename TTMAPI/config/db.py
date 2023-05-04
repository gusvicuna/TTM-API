import pymongo
from dotenv import dotenv_values


config = dotenv_values("settings.env")


def getDB():
    client = pymongo.MongoClient(
        config["CLIENT_URL"], uuidRepresentation="pythonLegacy")

    if (config["PROD_COLLECTION"] == "True"):
        db = client.production
    else:
        db = client.test

    return db
