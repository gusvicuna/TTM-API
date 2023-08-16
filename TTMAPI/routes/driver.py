from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.schemas.driver import\
    driverSchema, driversSchema
from TTMAPI.services import driver_service

router = APIRouter()
logger = get_logger(__name__)
base_route = "/drivers"


@router.get("")
async def find_all_drivers():
    logger.info("GET" + base_route)

    result = driver_service.get_all_drivers(logger=logger)
    return driversSchema(result)


@router.get('/{dbid}')
async def find_driver_by_name(dbid: str):
    logger.info(f"GET {base_route}/{dbid}")

    driver_cursor = driver_service.get_driver_by_id_service(
        dbid=dbid,
        logger=logger)

    driver = Driver(**driver_cursor)
    result = driverSchema(driver)
    return result


@router.post("")
async def create_driver(driver: Driver):
    driver = driverSchema(driver)
    logger.info(f"POST {base_route}  driver={driver}")

    result = driver_service.create_new_driver(
        driver=driver,
        logger=logger)
    return result


@router.put('/{dbid}')
async def update_driver(dbid: str, driver: Driver):
    driver = driverSchema(driver)
    logger.info(f"PUT {base_route}/{dbid}  driver={driver}")

    driver_result = driver_service.update_driver(
        driver=driver,
        dbid=dbid,
        logger=logger)
    if (driver_result is not None):
        result = Driver(**driver_result)
        result = driverSchema(result)
    else:
        result = driver_result
    return result


@router.delete('/{dbid}')
async def delete_driver(dbid: str):
    logger.info(f"DELETE {base_route}/{dbid}")

    result = driver_service.delete_driver(
        dbid=dbid,
        logger=logger)
    return result
