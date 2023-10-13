from fastapi import APIRouter, HTTPException

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.schemas.driver import (
    createDriverSchema,
    getDriverSchema,
    getDriversSchema)
from TTMAPI.services import MongoDB
from TTMAPI.services.OpenAI.generate_description import generate_description

router = APIRouter()
logger = get_logger(__name__)
base_route = "/drivers"


@router.get("")
async def find_all_drivers():
    logger.info("GET" + base_route)

    result = MongoDB.get_all_drivers(logger=logger)
    return getDriversSchema(result)


@router.post("")
async def create_driver(driver_input: Driver):

    logger.info(f"POST {base_route}  driver={driver_input}")

    driver_schema = createDriverSchema(driver_input)

    result = MongoDB.create_new_driver(
        driver=driver_schema,
        logger=logger)

    if not result:
        raise HTTPException(status_code=400, detail="Failed to create driver.")

    return result


@router.get('/{driver_id}')
async def find_driver_by_id(driver_id: int):
    logger.info(f"GET {base_route}/{driver_id}")

    driver_cursor = MongoDB.get_driver_by_id_service(
        driver_id=driver_id,
        logger=logger)

    driver = Driver(**driver_cursor)
    result = getDriverSchema(driver)
    return result


@router.put('/{driver_id}')
async def update_driver(driver_id: int, driver: Driver):
    driver = getDriverSchema(driver)
    logger.info(f"PUT {base_route}/{driver_id}  driver={driver}")

    driver_result = MongoDB.update_driver(
        driver=driver,
        driver_id=driver_id,
        logger=logger)
    if (driver_result is not None):
        result = Driver(**driver_result)
        result = getDriverSchema(result)
    else:
        result = driver_result
    return result


@router.delete('/{driver_id}')
async def delete_driver(driver_id: int):
    logger.info(f"DELETE {base_route}/{driver_id}")

    result = MongoDB.delete_driver(
        driver_id=driver_id,
        logger=logger)
    return result


@router.get("/{driver_id}/components/{component_id}/describe")
async def create_description(
        driver_id: int,
        component_id: int
        ):

    logger.info(f"GET {base_route}/create_description" +
                f" driver={driver_id}" +
                f" component={component_id}")

    driver_cursor = MongoDB.get_driver_by_id(
        driver_id=driver_id,
        logger=logger)
    driver = Driver(**driver_cursor)

    for component in driver.components:
        if component.id == component_id:
            selected_component = component

    selected_component.description = generate_description(
        name=selected_component.name,
        phrases=selected_component.phrases,
        logger=logger)

    driver_cursor = MongoDB.update_driver(
        driver=driver.dict(),
        driver_id=driver.id,
        logger=logger)
    driver = Driver(**driver_cursor)
    return driver
