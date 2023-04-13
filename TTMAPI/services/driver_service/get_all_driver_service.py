from TTMAPI.config.db import getDB


def get_all_drivers_service(logger, isProduction):
    db = getDB(isProduction=isProduction)
    try:
        drivers_cursor = db["drivers"].find()
    except Exception as e:
        logger.error(e)
        return None
    return drivers_cursor
