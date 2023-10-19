from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.schemas.process import getProcessedExperienceSchema
from TTMAPI.services import MongoDB
from TTMAPI.services.OpenAI.fix_grammar import fix_grammar
from TTMAPI.services.OpenAI.gpt_process import\
    gpt_process

router = APIRouter()
logger = get_logger(__name__)
base_route = "/process"


@router.post("/playground_process")
async def playground_process(
        trainText: str,
        beforeNegativeDistance: int = 15,
        afterNegativeDistance: int = 0,
        ttm: bool = True,
        gpt: bool = True,
        fixGrammar: bool = False
        ):

    logger.info(
        f"POST {base_route}/playground_process traintext='{trainText}' " +
        f" ttm={ttm} gpt={gpt}")

    if (fixGrammar):
        trainText = fix_grammar(traintext=trainText)
        logger.debug(f"fixed traintext ='{trainText}'")

    drivers_cursor = MongoDB.get_all_drivers(
        logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        if ttm:
            driver.AnalyzeText(
                trainText=trainText,
                beforeNegDis=int(beforeNegativeDistance),
                afterNegDis=int(afterNegativeDistance),
                complete=True)
        drivers.append(driver)

    if gpt:
        gpt_result = gpt_process(
            answer=trainText,
            drivers=drivers,
            logger=logger)
        for driver in drivers:
            if driver.id in gpt_result:
                for component in driver.components:
                    if component.id in gpt_result[driver.id]:
                        component.gpt_result =\
                            gpt_result[driver.id][component.id]

    result = getProcessedExperienceSchema(
        driver=drivers,
        experience=trainText)
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
                           afterNegDis=int(afterNegativeDistance),
                           complete=True)
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

    result = gpt_process(trainText, drivers=drivers, logger=logger)
    return result
