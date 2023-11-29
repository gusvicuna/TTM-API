from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.schemas.process import getProcessedExperienceSchema
from TTMAPI.services import MongoDB
from TTMAPI.services.OpenAI.fix_grammar import fix_grammar
from TTMAPI.services.OpenAI.gpt_process import\
    gpt_process
from TTMAPI.services.OpenAI.split_process import split_process

router = APIRouter()
logger = get_logger(__name__)
base_route = "/process"


@router.post("/playground_process")
async def playground_process(
        answer_text: str,
        answer_type: str,
        commerce_type: str = "comercio general",
        beforeNegativeDistance: int = 15,
        afterNegativeDistance: int = 0,
        ttm: bool = True,
        gpt: bool = True,
        model: str = "gpt-4",
        fixGrammar: bool = False,
        split_phrases: bool = False
        ):

    logger.info(
        f"POST {base_route}/playground_process traintext='{answer_text}' " +
        f"type={answer_type} ttm={ttm} gpt={gpt}")

    if (fixGrammar):
        answer_text = fix_grammar(traintext=answer_text)

    drivers_cursor = MongoDB.get_all_drivers(
        logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        if ttm:
            driver.AnalyzeText(
                trainText=answer_text,
                beforeNegDis=int(beforeNegativeDistance),
                afterNegDis=int(afterNegativeDistance),
                complete=True)
        drivers.append(driver)

    if gpt:
        if split_phrases:
            gpt_result = split_process(
                answer_text=answer_text,
                answer_type=answer_type,
                commerce_type=commerce_type,
                drivers=drivers,
                model=model,
                logger=logger)
        else:
            gpt_result, exception = gpt_process(
                answer_text=answer_text,
                answer_type=answer_type,
                commerce_type=commerce_type,
                model=model,
                drivers=drivers,
                logger=logger)
            if exception:
                raise exception
        for driver in drivers:
            if driver.id in gpt_result:
                for component in driver.components:
                    if component.id in gpt_result[driver.id]:
                        component.gpt_result =\
                            gpt_result[driver.id][component.id]

    result = getProcessedExperienceSchema(
        driver=drivers,
        experience=answer_text)
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

    drivers_cursor = MongoDB.get_all_drivers(logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        drivers.append(driver)

    result = gpt_process(trainText, drivers=drivers, logger=logger)
    return result


@router.get("/create_csv_of_aceptions")
async def create_csv_of_aceptions():

    logger.info(f"GET {base_route}/create_csv_of_aceptions")

    MongoDB.drivers_and_components_to_csv(logger=logger)
