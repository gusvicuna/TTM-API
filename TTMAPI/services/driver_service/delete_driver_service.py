from TTMAPI.config.db import getDB
from fastapi import HTTPException


def delete_driver_service(dbid: str, logger):
    db = getDB()
    try:
        driver_cursor = db["drivers"].find_one({"dbid": dbid})
        if driver_cursor is not None:
            db["drivers"].delete_one({"dbid": dbid})
            return "OK"
        else:
            raise HTTPException(status_code=404, detail="Driver not found")
    except Exception as e:
        logger.error(e)
        return None