from TTMAPI.models.component import Component
from TTMAPI.models.driver import Driver
from TTMAPI.models.sqlalchemy_models import Answer, Survey
from TTMAPI.services.OpenAI.gpt_simple_process import gpt_simple_process
from TTMAPI.services.PostgreSQL.upsert_answer_component_service import\
    upsert_answer_component


def process_answer(session, logger):

    answer: Answer = session.query(Answer).filter_by(
        has_been_processed=False).first()

    survey: Survey = answer.survey
    sql_drivers = survey.drivers

    drivers = []
    for sql_driver in sql_drivers:
        driver = Driver(id=sql_driver.id, name=sql_driver.name)
        if (sql_driver.type == "ut"):
            driver.isUT = True
        for sql_component in sql_driver.components:
            component = Component(
                name=sql_component.name,
                id=sql_component.id
                # description=component_sql.description,
                )
            for aception in sql_component.aceptions:
                component.phrases.append(aception.phrase)
            driver.components.append(component)
        drivers.append(driver)

    gpt_results = gpt_simple_process(
        answer=answer.answer_text,
        drivers=drivers,
        logger=logger)

    for driver_id in gpt_results:
        driver = next(obj for obj in drivers if obj.id == driver_id)
        for component_id in gpt_results[driver_id]:
            component = next(
                obj for obj in driver.components if obj.id == component_id)
            component.gpt_result = gpt_results[driver_id][component_id]
            component.TextMatch(answer.answer_text)
            component.SetPolar()
            upsert_answer_component(
                session=session,
                component=component,
                survey_id=survey.id,
                driver_id=driver.id,
                token=answer.token)
    answer.has_been_processed = True
    session.commit()
