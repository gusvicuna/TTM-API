from fastapi import APIRouter, Depends

from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.models.driver import Driver
from TTMAPI.schemas.process import playgroundResponseSchema
from TTMAPI.services import Playground
from TTMAPI.services.OpenAIServices.fix_grammar import fix_grammar
from TTMAPI.services.OpenAIServices.gpt_process import\
    gpt_process
from TTMAPI.services.OpenAIServices.split_process import split_process

router = APIRouter()
logger = get_logger(__name__)
base_route = "/process"


@router.post("/playground_process")
async def playground_process(
        answer_text: str,
        answer_type: str,
        commerce_type: str,
        beforeNegativeDistance: int = 15,
        afterNegativeDistance: int = 0,
        ttm: bool = True,
        gpt: bool = True,
        model: str = "gpt-4",
        fixGrammar: bool = False,
        convertToChilean: bool = False,
        traductionToSpanish: bool = True,
        split_phrases: bool = False,
        session=Depends(getPostgreSQL)
        ):

    logger.info(
        f"POST {base_route}/playground_process traintext='{answer_text}' " +
        f"type={answer_type} ttm={ttm} gpt={gpt}")

    if (fixGrammar):
        answer_text = fix_grammar(
            originalText=answer_text,
            convertToChilean=convertToChilean,
            traductionToSpanish=traductionToSpanish,
            session=session,
            logger=logger)

    drivers_cursor = Playground.get_all_drivers(
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

    in_tokens = 0
    out_tokens = 0
    if gpt:
        if split_phrases:
            gpt_result, exceptions, in_tokens, out_tokens = split_process(
                session=session,
                answer_text=answer_text,
                answer_type=answer_type,
                commerce_type=commerce_type,
                drivers=drivers,
                model=model,
                logger=logger)
            if exceptions:
                for exception in exceptions:
                    raise exception
        else:
            gpt_result, exception, in_tokens, out_tokens = gpt_process(
                session=session,
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

    result = playgroundResponseSchema(
        driver=drivers,
        experience=answer_text,
        input_tokens=in_tokens,
        output_tokens=out_tokens,
        model=model)
    return result


@router.post("/ttm_simple")
async def get_TTM_simple_match(
        trainText: str,
        beforeNegativeDistance: int = 100,
        afterNegativeDistance: int = 100,
        fixGrammar: bool = False,
        session=Depends(getPostgreSQL)
        ):

    logger.info(f"POST {base_route}/ttm_simple  traintext='{trainText}'")

    if (fixGrammar):
        trainText = fix_grammar(
            originalText=trainText,
            convertToChilean=False,
            traductionToSpanish=False,
            session=session,
            logger=logger)
        logger.info(f"fixed traintext ='{trainText}'")

    drivers_cursor = Playground.get_all_drivers(
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
        fixGrammar: bool = False,
        session=Depends(getPostgreSQL)
        ):

    logger.info(f"POST {base_route}/gpt_simple  traintext='{trainText}'")

    if (fixGrammar):
        trainText = fix_grammar(
            originalText=trainText,
            convertToChilean=False,
            traductionToSpanish=False,
            session=session,
            logger=logger)

    drivers_cursor = Playground.get_all_drivers(logger=logger)
    drivers = []
    for driver_cursor in drivers_cursor:
        driver = Driver(**driver_cursor)
        drivers.append(driver)

    gpt_result, exception, tokens = gpt_process(
                session=session,
                answer_text=trainText,
                answer_type="MB",
                commerce_type="general",
                model="gpt-4",
                drivers=drivers,
                logger=logger)
    if exception:
        raise exception
    return gpt_result


@router.get("/create_csv_of_aceptions")
async def create_csv_of_aceptions():

    logger.info(f"GET {base_route}/create_csv_of_aceptions")

    Playground.drivers_and_components_to_csv(logger=logger)
