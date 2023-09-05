from TTMAPI.config.db import getMongo
from fastapi import HTTPException


def get_driver_by_id_service(dbid: str, logger):
    db = getMongo()
    try:
        driver_cursor = db["drivers"].find_one({"dbid": dbid})
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)

    if driver_cursor is not None:
        return driver_cursor
    else:
        raise HTTPException(status_code=404, detail="Driver not found")
