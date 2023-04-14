from TTMAPI.config.db import getDB
from TTMAPI.models.driver import Driver


def update_driver_service(driver: Driver, name: str, logger):
    collection = getDB().drivers
    try:
        driver_cursor = collection.find_one({"name": name})
        if (driver_cursor is None):
            raise Exception("No Driver with that name")

        collection.replace_one(
            {"name": name},
            driver)
        driver_cursor = collection.find_one({"name": name})

    except Exception as e:
        logger.error(e)
        return None
    return driver_cursor
