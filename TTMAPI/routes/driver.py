from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.schemas.driver import driverEntity, driversEntity
from TTMAPI.services import driver_service

router = APIRouter()
logger = get_logger(__name__)
base_route = "/drivers"


@router.get(base_route)
async def find_all_drivers():
    logger.info("GET" + base_route)

    result = driver_service.get_all_drivers(logger=logger)
    return driversEntity(result)


@router.get(base_route + '/{name}')
async def find_driver_by_name(name):
    logger.info("GET" + base_route + f"/{name}")

    driver_cursor = driver_service.get_driver_by_id_service(
        name=name, logger=logger)

    driver = Driver(**driver_cursor)
    result = driverEntity(driver)
    return result


@router.post(base_route)
async def create_driver(driver: Driver):
    logger.info(f"POST {base_route}  driver={driver}")

    result = driver_service.create_new_driver(
        driver=driver, logger=logger)
    return result


@router.put(base_route + '/{name}')
async def update_driver(name, driver: Driver):
    logger.info(f"PUT {base_route}/{name}  driver={driver}")

    result = driver_service.update_driver(
        driver=driver, name=name, logger=logger)
    return result
