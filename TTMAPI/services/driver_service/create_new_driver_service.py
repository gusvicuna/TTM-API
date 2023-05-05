from TTMAPI.config.db import getDB
from TTMAPI.models.driver import Driver
from fastapi import HTTPException

import uuid


def create_new_driver_service(driver: Driver, logger):
    db = getDB()
    try:
        driver["dbid"] = str(uuid.uuid4())
        result = db["drivers"].insert_one(driver)
        return result
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
