from fastapi import APIRouter, Body, Depends, status

from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.services.PostgreSQL.get_processed_answers_service import (
    get_processed_answer)
from TTMAPI.services.PostgreSQL.upsert_aception_service import upsert_aception
from TTMAPI.services.PostgreSQL.upsert_answer_service import upsert_answer
from TTMAPI.services.PostgreSQL.upsert_component_service import (
    upsert_component)
from TTMAPI.services.PostgreSQL.upsert_driver_service import upsert_driver
from TTMAPI.services.PostgreSQL.upsert_survey_service import upsert_survey
from TTMAPI.services.PostgreSQL.process_answer_service import process_answer

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
                            driver=driver
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

    return answer_tokens


@router.get("/process_answer", status_code=status.HTTP_200_OK)
async def process_answer_by_token(
        session=Depends(getPostgreSQL)
        ):
    return process_answer(session=session, logger=logger)


@router.post("/processed_answers")
async def get_processed_answers(
        data: list = Body(...),
        session=Depends(getPostgreSQL)
        ):

    logger.info(f"GET {base_route}/processed_answers items={data}")

    results = []
    for token in data:
        results.append(get_processed_answer(
            token=token,
            session=session,
            logger=logger))
    return results
