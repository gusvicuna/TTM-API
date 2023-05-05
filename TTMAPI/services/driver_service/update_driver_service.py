from TTMAPI.config.db import getDB
from TTMAPI.models.driver import Driver
from fastapi import HTTPException


def update_driver_service(driver: Driver, dbid: str, logger):
    collection = getDB().drivers

    driver_cursor = collection.find_one({"dbid": dbid})
    if driver_cursor is not None:

        try:
            for component in driver["components"]:
                if "" in component["phrases"]:
                    component["phrases"].remove("")
                if " " in component["phrases"]:
                    component["phrases"].remove(" ")

            collection.replace_one(
                {"dbid": dbid},
                driver)

            return collection.find_one({"dbid": dbid})
        except Exception as e:
            logger.error(f"Error: {e}")
            raise HTTPException(status_code=500, detail=e)

    else:
        logger.error("Driver not Found")
        raise HTTPException(status_code=404, detail="Driver not found")
