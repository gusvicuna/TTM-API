from TTMAPI.config.db import getMongo
from fastapi import HTTPException


def get_all_drivers_service(logger):
    """
    Get all drivers from MongoDB.
    Order them by driver_type.
    """
    db = getMongo()
    try:
        drivers_cursor = db["drivers"].find().sort("id", 1)
        drivers_cursor = drivers_cursor.sort("driver_type", 1)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    return drivers_cursor
