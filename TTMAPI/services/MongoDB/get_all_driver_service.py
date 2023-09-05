from TTMAPI.config.db import getMongo
from fastapi import HTTPException


def get_all_drivers_service(logger):
    db = getMongo()
    try:
        drivers_cursor = db["drivers"].find()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    return drivers_cursor
