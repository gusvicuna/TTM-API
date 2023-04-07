from TTMAPI.config.db import getDB
from TTMAPI.models.driver import Driver


def update_driver_service(driver: Driver, name: str, logger):
    db = getDB()
    try:
        db["drivers"].replace_one(
            {"name": name},
            driver.dict(),
            {"writeConcern": {"w": "majority", "wtimeout": 5000}})
    except Exception as e:
        logger.error(e)
        return e
    return "OK"
