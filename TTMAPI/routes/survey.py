from fastapi import APIRouter, Body, Depends, status

from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.services.PostgreSQL.insert_aception_service import insert_aception
from TTMAPI.services.PostgreSQL.insert_answer_service import insert_answer
from TTMAPI.services.PostgreSQL.insert_component_service import (
    insert_component)
from TTMAPI.services.PostgreSQL.insert_driver_service import insert_driver
from TTMAPI.services.PostgreSQL.insert_survey_service import upsert_survey

router = APIRouter()
logger = get_logger(__name__)
base_route = "/surveys"


@router.post("",
             status_code=status.HTTP_200_OK)
async def create_surveys(
        data: list = Body(...),
        session=Depends(getPostgreSQL)
        ):

    logger.info(f"POST {base_route}/surveys/ items={data}")

    answer_tokens = []
    for survey_data in data:
        survey = upsert_survey(
            session=session,
            survey_data=survey_data,
            logger=logger)

        for driver_data in survey_data["drivers"]:
            driver = insert_driver(
                session=session,
                driver_data=driver_data,
                survey=survey,
                driver_type="driver",
                logger=logger)
            for component_data in driver_data["components"]:
                component = insert_component(
                    session=session,
                    component_data=component_data,
                    driver=driver,
                    logger=logger
                )
                for aception in component_data["aceptions"]:
                    insert_aception(
                        session=session,
                        phrase=aception,
                        component=component,
                        logger=logger
                    )
        for like_data in survey_data["like"]:
            driver = insert_driver(
                session=session,
                driver_data=like_data,
                survey=survey,
                driver_type="like",
                logger=logger)
            for component_data in driver_data["components"]:
                component = insert_component(
                    session=session,
                    component_data=component_data,
                    driver=driver,
                    logger=logger
                )
                for aception in component_data["aceptions"]:
                    insert_aception(
                        session=session,
                        phrase=aception,
                        component=component,
                        logger=logger
                    )
        for ut_data in survey_data["ut"]:
            driver = insert_driver(
                session=session,
                driver_data=ut_data,
                survey=survey,
                driver_type="ut",
                logger=logger)
            for component_data in ut_data["components"]:
                component = insert_component(
                    session=session,
                    component_data=component_data,
                    driver=driver,
                    logger=logger)
                for aception in component_data["aceptions"]:
                    insert_aception(
                        session=session,
                        phrase=aception,
                        component=component,
                        logger=logger
                    )

        for answer_data in survey_data["answers"]:
            answer = insert_answer(
                session=session,
                answer_data=answer_data,
                survey=survey,
                logger=logger)
            answer_tokens.append(answer.token)

    session.commit()
    return answer_tokens
