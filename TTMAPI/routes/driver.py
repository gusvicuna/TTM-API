from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.schemas.driver import\
    driverSchema, driversSchema, matchedDriversSchema
from TTMAPI.services import driver_service
from TTMAPI.services.OpenAI.fix_grammar import fix_grammar


router = APIRouter()
logger = get_logger(__name__)
base_route = "/drivers"


@router.get(base_route)
async def find_all_drivers():
    logger.info("GET" + base_route)

    result = driver_service.get_all_drivers(logger=logger)
    return driversSchema(result)


@router.get(base_route + '/{dbid}')
async def find_driver_by_name(dbid: str):
    logger.info(f"GET {base_route}/{dbid}")

    driver_cursor = driver_service.get_driver_by_id_service(
        dbid=dbid,
        logger=logger)

    driver = Driver(**driver_cursor)
    result = driverSchema(driver)
    return result


@router.post(base_route)
async def create_driver(driver: Driver):
    driver = driverSchema(driver)
    logger.info(f"POST {base_route}  driver={driver}")

    result = driver_service.create_new_driver(
        driver=driver,
        logger=logger)
    return result


@router.put(base_route + '/{dbid}')
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


@router.delete(base_route + '/{dbid}')
async def delete_driver_service(dbid: str):
    logger.info(f"DELETE {base_route}/{dbid}")

    result = driver_service.delete_driver(
        dbid=dbid,
        logger=logger)
    return result


@router.post(base_route + "/match")
async def get_matched_drivers(
        trainText: str,
        beforeNegativeDistance: int = 100,
        afterNegativeDistance: int = 100,
        fixGrammar: bool = False
        ):

    logger.info(f"POST {base_route}/match  traintext='{trainText}'")

    # if (fixGrammar):
    #     trainText = fix_grammar(traintext=trainText)
    #     logger.info(f"fixed traintext ='{trainText}'")

    drivers_cursor = driver_service.get_all_drivers(
        logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        driver.AnalyzeText(trainText=trainText,
                           beforeNegDis=int(beforeNegativeDistance),
                           afterNegDis=int(afterNegativeDistance))
        drivers.append(driver)

    result = matchedDriversSchema(drivers)
    return result


@router.post(base_route + "/dbmatch")
async def get_db_match(
        trainText: str,
        beforeNegativeDistance: int = 100,
        afterNegativeDistance: int = 100,
        fixGrammar: bool = False
        ):

    logger.info(f"POST {base_route}/dbmatch  traintext='{trainText}'")

    # if (fixGrammar):
    #     trainText = fix_grammar(traintext=trainText)
    #     logger.info(f"fixed traintext ='{trainText}'")

    drivers_cursor = driver_service.get_all_drivers(
        logger=logger)
    components = {}
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        driver.AnalyzeText(trainText=trainText,
                           beforeNegDis=int(beforeNegativeDistance),
                           afterNegDis=int(afterNegativeDistance))
        for component in driver.components:
            components[component.name] = component.mark

    return components
