from fastapi import HTTPException
from TTMAPI.models.sqlalchemy_models import Driver


def insert_driver(session, driver_data, survey, driver_type, logger):
    try:
        driver = Driver(
            name=driver_data["name"],
            type=driver_type,
            survey=survey)
        session.add(driver)
        session.flush()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    return driver
