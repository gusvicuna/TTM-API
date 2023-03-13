from TTMAPI.config.db import getDB


def get_driver_by_id_service(name: str, logger):
    db = getDB()
    try:
        driver_cursor = db["drivers"].find_one({"name": name})
    except Exception as e:
        logger.error(e)
        return None

    return driver_cursor
