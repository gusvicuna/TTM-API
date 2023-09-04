from TTMAPI.config.db import getDB
from TTMAPI.models.driver import Driver
from fastapi import HTTPException

import uuid


def create_new_driver_service(driver: Driver, logger):
    db = getDB()
    try:
        driver["dbid"] = str(uuid.uuid4())
        db["drivers"].insert_one(driver)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
