from TTMAPI.config.db import getDB
from TTMAPI.models.driver import Driver


def create_new_driver_service(driver: Driver, logger):
    db = getDB()
    try:
        db["drivers"].insert_one(driver.dict())
    except Exception as e:
        logger.error(e)
        return e
    return "OK"
