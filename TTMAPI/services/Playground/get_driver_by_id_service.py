from TTMAPI.config.db import getMongo
from fastapi import HTTPException


def get_driver_by_id_service(driver_id: str, logger):
    db = getMongo()
    try:
        driver_cursor = db["drivers"].find_one({"id": driver_id})
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)

    if not driver_cursor:
        raise HTTPException(status_code=404, detail="Driver not found")

    return driver_cursor
