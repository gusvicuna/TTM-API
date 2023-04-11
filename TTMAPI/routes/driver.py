from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.models.aception import Aception
from TTMAPI.schemas.driver import\
    driverSchema, driversSchema, matchedDriversSchema
from TTMAPI.services import driver_service


router = APIRouter()
logger = get_logger(__name__)
base_route = "/drivers"


@router.get(base_route)
async def find_all_drivers():
    logger.info("GET" + base_route)

    result = driver_service.get_all_drivers(logger=logger)
    return driversSchema(result)


@router.get(base_route + '/{name}')
async def find_driver_by_name(name):
    logger.info("GET" + base_route + f"/{name}")

    driver_cursor = driver_service.get_driver_by_id_service(
        name=name, logger=logger)

    driver = Driver(**driver_cursor)
    result = driverSchema(driver)
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

    driver_result = driver_service.update_driver(
        driver=driver, name=name, logger=logger)
    if (driver_result is not None):
        result = Driver(**driver_result)
        result = driverSchema(result)
    else:
        result = driver_result
    return result


@router.post(base_route + "/match")
async def get_matched_drivers(aception: Aception):
    logger.info(f"POST {base_route}/match  aception='{aception.text}'")

    drivers_cursor = driver_service.get_all_drivers(logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        driver.GetBestPercents(aception)
        drivers.append(driver)

    result = matchedDriversSchema(drivers)
    return result
