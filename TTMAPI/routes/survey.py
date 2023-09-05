from fastapi import APIRouter, Body, Depends, status

from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.services.PostgreSQL.insert_aception_service import insert_aception
from TTMAPI.services.PostgreSQL.insert_answer_service import insert_answer
from TTMAPI.services.PostgreSQL.insert_component_service import (
    insert_component)
from TTMAPI.services.PostgreSQL.insert_driver_service import insert_driver
from TTMAPI.services.PostgreSQL.insert_survey_service import insert_survey

router = APIRouter()
logger = get_logger(__name__)
base_route = "/surveys"


@router.post("",
             status_code=status.HTTP_201_CREATED)
async def create_surveys(
        data: list = Body(...),
        session=Depends(getPostgreSQL)
        ):

    logger.info(f"POST {base_route}/surveys/ items={data}")

    for survey_data in data:
        survey = insert_survey(
            session=session,
            survey_data=survey_data)

        for driver_data in survey_data["drivers"]:
            driver = insert_driver(
                session=session,
                driver_data=driver_data,
                survey=survey,
                driver_type="driver")
            for component_data in driver_data["components"]:
                component = insert_component(
                    session=session,
                    component_data=component_data,
                    driver=driver
                )
                for aception in component_data["aceptions"]:
                    insert_aception(
                        session=session,
                        phrase=aception,
                        component=component
                    )
        for like_data in survey_data["like"]:
            driver = insert_driver(
                session=session,
                driver_data=like_data,
                survey=survey,
                driver_type="like")
            for component_data in driver_data["components"]:
                component = insert_component(
                    session=session,
                    component_data=component_data,
                    driver=driver
                )
                for aception in component_data["aceptions"]:
                    insert_aception(
                        session=session,
                        phrase=aception,
                        component=component
                    )
        for ut_data in survey_data["ut"]:
            driver = insert_driver(
                session=session,
                driver_data=ut_data,
                survey=survey,
                driver_type="ut")
            for component_data in ut_data["components"]:
                component = insert_component(
                    session=session,
                    component_data=component_data,
                    driver=driver)
                for aception in component_data["aceptions"]:
                    insert_aception(
                        session=session,
                        phrase=aception,
                        component=component
                    )

        for answer_data in survey_data["answers"]:
            insert_answer(
                session=session,
                answer_data=answer_data,
                survey=survey)

    session.commit()
