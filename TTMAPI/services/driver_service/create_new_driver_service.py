from TTMAPI.config.db import getDB
from TTMAPI.models.driver import Driver

import uuid


def create_new_driver_service(driver: Driver, logger):
    db = getDB()
    try:
        driver["dbid"] = str(uuid.uuid4())
        result = db["drivers"].insert_one(driver)
    except Exception as e:
        logger.error(e)
        return e
    return result.acknowledged
