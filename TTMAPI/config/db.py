import pymongo
from dotenv import dotenv_values


config = dotenv_values("settings.env")


def getDB(isProduction: bool = True):
    client = pymongo.MongoClient(
        config["CLIENT_URL"], uuidRepresentation="pythonLegacy")

    if (isProduction):
        db = client.production
    else:
        db = client.test

    return db
