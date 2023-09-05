import pymongo
from dotenv import dotenv_values
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


config = dotenv_values("settings.env")

engine = create_engine(config["POSTGRE_URL"])
SessionLocal = sessionmaker(bind=engine)


def getMongo():
    client = pymongo.MongoClient(
        config["CLIENT_URL"], uuidRepresentation="pythonLegacy")

    if (config["PROD_COLLECTION"] == "True"):
        db = client.production
    else:
        db = client.test

    return db


def getPostgreSQL():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
