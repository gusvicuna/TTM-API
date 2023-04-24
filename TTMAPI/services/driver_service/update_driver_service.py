from TTMAPI.config.db import getDB
from TTMAPI.models.driver import Driver
from fastapi import HTTPException


def update_driver_service(driver: Driver, dbid: str, logger):
    collection = getDB().drivers
    driver_cursor = collection.find_one({"dbid": dbid})
    if driver_cursor is not None:
        collection.replace_one(
            {"dbid": dbid},
            driver)
        return collection.find_one({"dbid": dbid})
    else:
        raise HTTPException(status_code=404, detail="Driver not found")
