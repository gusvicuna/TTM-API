from fastapi import APIRouter, Body, Depends, HTTPException, status

from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.jobs.create_descriptions_job import create_descriptions
from TTMAPI.services.PostgreSQL.get_processed_answers_service import (
    get_processed_answer)
from TTMAPI.services.PostgreSQL.upsert_aception_service import upsert_aception
from TTMAPI.services.PostgreSQL.upsert_answer_service import upsert_answer
from TTMAPI.services.PostgreSQL.upsert_component_service import (
    upsert_component)
from TTMAPI.services.PostgreSQL.upsert_driver_service import upsert_driver
from TTMAPI.services.PostgreSQL.upsert_survey_service import upsert_survey
from TTMAPI.services.PostgreSQL.process_answer_service import process_answer
from TTMAPI.services.PostgreSQL.get_answer_service import get_answer

router = APIRouter()
logger = get_logger(__name__)
base_route = "/surveys"


@router.post("", status_code=status.HTTP_200_OK)
async def create_surveys(
        data: list = Body(...),
        session=Depends(getPostgreSQL)
        ):
    """
    Create new surveys along with their related subcomponents
    (drivers, components, aceptions, and answers).
    """

    logger.info(f"POST {base_route}/surveys/ items={data}")

    answer_tokens = []
    try:
        for survey_data in data:
            # Upsert survey data
            survey = upsert_survey(
                session=session,
                survey_data=survey_data
                )

            # Iterate through all driver types and upsert data
            for driver_type in ["drivers", "like", "ut"]:
                for driver_data in survey_data.get(driver_type, []):

                    # Set the driver type based on the key
                    driver_data["type"] = driver_type
                    driver = upsert_driver(
                        session=session,
                        driver_data=driver_data,
                        survey=survey
                    )

                    for component_data in driver_data.get("components", []):
                        component = upsert_component(
                            session=session,
                            component_data=component_data,
                            driver=driver,
                            logger=logger
                        )
                        for aception_phrase in component_data.get(
                                "aceptions", []):
                            upsert_aception(
                                session=session,
                                phrase=aception_phrase,
                                component=component
                            )

            # Upsert answer data
            for answer_data in survey_data.get("answers", []):
                answer = upsert_answer(
                    session=session,
                    answer_data=answer_data,
                    survey=survey,
                    )
                answer_tokens.append(answer.token)

        session.commit()

    except Exception as e:
        session.rollback()  # Rollback transaction in case of error
        logger.error(f"Failed to create surveys: {e}")
        raise

    finally:
        session.close()

    return answer_tokens


@router.get("/process_answer", status_code=status.HTTP_200_OK)
async def process_answer_by_token(
        session=Depends(getPostgreSQL)
        ):
    try:
        result = process_answer(session=session, logger=logger)
    except Exception as e:
        raise HTTPException(detail=e, status_code=500)
    finally:
        session.close()
    return result


@router.get("/describe_survey", status_code=status.HTTP_200_OK)
async def describe_survey(
        session=Depends(getPostgreSQL)
        ):
    return create_descriptions()


@router.post("/processed_answers")
async def get_processed_answers(
        data: list = Body(...),
        session=Depends(getPostgreSQL)
        ):

    logger.info(f"GET {base_route}/processed_answers items={data}")

    results = []
    try:
        for token in data:
            results.append(get_processed_answer(
                token=token,
                session=session,
                logger=logger))
    finally:
        session.close()
    return results

# Create endpoit for resetting the results of a list of answers
@router.post("/reset_answers")
async def reset_answers(
        data: list = Body(...),
        session=Depends(getPostgreSQL)
        ):

    logger.info(f"POST {base_route}/reset_answers items={data}")

    try:
        for token in data:
            answer = get_answer(session=session, token=token, logger=logger)
            answer.has_been_processed = False
            session.commit()
    finally:
        session.close()
    return {"message": "success"}
