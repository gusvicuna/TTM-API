from TTMAPI.config.db import getMongo
from fastapi import HTTPException


def delete_driver_service(driver_id: str, logger):
    db = getMongo()
    try:
        driver_cursor = db["drivers"].find_one({"id": driver_id})
        if driver_cursor is not None:
            db["drivers"].delete_one({"id": driver_id})
            return "OK"
        else:
            raise HTTPException(status_code=404, detail="Driver not found")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=e)
