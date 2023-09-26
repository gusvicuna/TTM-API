from TTMAPI.config.db import getMongo
from TTMAPI.models.driver import Driver
from fastapi import HTTPException


def update_driver_service(driver: Driver, driver_id: str, logger):
    collection = getMongo().drivers

    driver_cursor = collection.find_one({"id": driver_id})
    if driver_cursor is not None:

        try:
            for component in driver["components"]:
                if "" in component["phrases"]:
                    component["phrases"].remove("")
                if " " in component["phrases"]:
                    component["phrases"].remove(" ")

            collection.replace_one(
                {"id": driver_id},
                driver)

            return collection.find_one({"id": driver_id})
        except Exception as e:
            logger.error(f"Error: {e}")
            raise HTTPException(status_code=500, detail=e)

    else:
        logger.error("Driver not Found")
        raise HTTPException(status_code=404, detail="Driver not found")
