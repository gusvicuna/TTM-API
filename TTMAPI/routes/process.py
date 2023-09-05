from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.schemas.driver import matchedDriversSchema
from TTMAPI.services import MongoDB
from TTMAPI.services.OpenAI.fix_grammar import fix_grammar
from TTMAPI.services.OpenAI.API.gpt_simple_process import\
    gpt_simple_process
from TTMAPI.services.OpenAI.API.generate_description import\
    generate_description

router = APIRouter()
logger = get_logger(__name__)
base_route = "/process"


@router.post("/playground_process")
async def post_playground_process(
        trainText: str,
        beforeNegativeDistance: int = 15,
        afterNegativeDistance: int = 0,
        ttm_process: bool = True,
        gpt_process: bool = False,
        fixGrammar: bool = False
        ):

    logger.info(
        f"POST {base_route}/playground_process traintext='{trainText}' " +
        " ttm_process={ttm_process} gpt_process={gpt_process}")

    if (fixGrammar):
        trainText = fix_grammar(traintext=trainText)
        logger.debug(f"fixed traintext ='{trainText}'")

    drivers_cursor = MongoDB.get_all_drivers(
        logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        if ttm_process:
            driver.AnalyzeText(
                trainText=trainText,
                beforeNegDis=int(beforeNegativeDistance),
                afterNegDis=int(afterNegativeDistance))
        drivers.append(driver)

    if gpt_process:
        gpt_result = gpt_simple_process(
            trainText,
            drivers=drivers,
            logger=logger)
        for driver in drivers:
            for component in driver.components:
                component.gpt_result = gpt_result[component.name]

    result = matchedDriversSchema(drivers)
    return result


@router.post("/ttm_simple")
async def get_TTM_simple_match(
        trainText: str,
        beforeNegativeDistance: int = 100,
        afterNegativeDistance: int = 100,
        fixGrammar: bool = False
        ):

    logger.info(f"POST {base_route}/ttm_simple  traintext='{trainText}'")

    if (fixGrammar):
        trainText = fix_grammar(traintext=trainText)
        logger.info(f"fixed traintext ='{trainText}'")

    drivers_cursor = MongoDB.get_all_drivers(
        logger=logger)
    components = {}
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        driver.AnalyzeText(trainText=trainText,
                           beforeNegDis=int(beforeNegativeDistance),
                           afterNegDis=int(afterNegativeDistance))
        for component in driver.components:
            components[component.name] = component.ttm_result

    return components


@router.post("/gpt_simple")
async def get_GPT_simple_match(
        trainText: str,
        fixGrammar: bool = False
        ):

    logger.info(f"POST {base_route}/gpt_simple  traintext='{trainText}'")

    if (fixGrammar):
        trainText = fix_grammar(traintext=trainText)
        logger.debug(f"fixed traintext ='{trainText}'")

    drivers_cursor = MongoDB.get_all_drivers(logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        drivers.append(driver)

    result = gpt_simple_process(trainText, drivers=drivers, logger=logger)
    return result


@router.post("/create_description")
async def create_description(
        component_name: str
        ):

    logger.info(f"POST {base_route}/create_description" +
                " component_name='{component_name}'")

    drivers_cursor = MongoDB.get_all_drivers(logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        drivers.append(driver)

    for driver in drivers:
        for component in driver.components:
            if component.name == component_name:
                selected_component = component

    selected_component.description = generate_description(
        name=selected_component.name,
        phrases=selected_component.phrases,
        logger=logger)
    for driver in drivers:
        for component in driver.components:
            if component.name == component_name:
                MongoDB.update_driver(
                    driver=driver.dict(),
                    dbid=driver.dbid,
                    logger=logger)
