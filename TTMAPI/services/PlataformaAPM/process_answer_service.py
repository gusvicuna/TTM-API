from typing import List
from sqlalchemy.exc import SQLAlchemyError

from TTMAPI.models.component import Component
from TTMAPI.models.driver import Driver
from TTMAPI.models.sqlalchemy_models import Answer, Survey
from TTMAPI.services.OpenAIServices.gpt_process import (
    gpt_process)
from TTMAPI.services.OpenAIServices.split_process import split_process
from TTMAPI.services.OpenAIServices.fix_grammar import fix_grammar
from TTMAPI.services.PlataformaAPM.upsert_answer_component_service import\
    upsert_answer_component
from TTMAPI.services.PlataformaAPM.insert_error_process_service import (
    insert_error_process)
from TTMAPI.services.PlataformaAPM.upsert_answer_service import upsert_answer


def process_answer(session, logger):
    # Se busca una respuesta sin procesar
    try:
        surveys: List[Survey] = session.query(Survey).filter_by(
            has_been_described=True
        ).all()
    except Exception as e:
        logger.error(f"Error obteniendo encuestas. Error: {e}")
        session.rollback()
        return f"Error obteniendo encuestas. Error: {e}"
    if not surveys:
        logger.info("No se encuentran encuestas ya descritas.")
        return "No se encuentran encuestas ya descritas."
    survey: Survey = None
    for survey_sql in surveys:
        answer: Answer = None
        for answer_sql in survey_sql.answers:
            if not answer_sql.has_been_processed:
                answer = answer_sql
        if answer:
            survey = survey_sql
            break
    if not survey:
        logger.info("No se encuentran respuestas sin procesar.")
        return "No se encuentran respuestas sin procesar."
    logger.info(
        "Procesando respuesta con\n" +
        f"Token: {answer.token}.\n" +
        f"Text: {answer.answer_text}")

    # Se corrige la gramática de la respuesta
    fixed_answer = fix_grammar(
        originalText=answer.answer_text,
        convertToChilean=False,
        traductionToSpanish=True,
        session=session,
        logger=logger)

    # Se convierten los drivers de la encuesta a drivers de la API,
    # y se procesa la respuesta con TTM para cada uno
    sql_drivers = survey.drivers
    drivers = []
    try:
        for sql_driver in sql_drivers:
            driver = Driver(id=sql_driver.id, name=sql_driver.name)
            driver.driver_type = sql_driver.type
            for sql_component in sql_driver.components:
                component = Component(
                    name=sql_component.name,
                    id=sql_component.id,
                    description=sql_component.description,
                    )
                for aception in sql_component.aceptions:
                    component.phrases.append(aception.phrase)
                driver.components.append(component)
            driver.AnalyzeText(
                trainText=fixed_answer,
                beforeNegDis=15,
                afterNegDis=0,
                complete=False)
            drivers.append(driver)
        # Se marca el componente default de TTM
        for driver in drivers:
            if driver.id == survey.default_ut_driver_id:
                for component in driver.components:
                    if component.id == survey.default_ut_component_id:
                        component.ttm_result = 1
                        break
    except Exception as e:
        error_text = f"Error con TTM process. Error: {e}"
        logger.error(error_text)
        session.rollback()
        handle_error(session, answer, error_text, logger)
        return error_text

    # Se procesa la respuesta con GPT
    # el tipo de proceso dependiendo de la cantidad de palabras
    words_in_answer = len(fixed_answer.split(" "))
    if words_in_answer > 5:
        # if words_in_answer <= 7:
        model = "gpt-3.5-turbo-1106"
        # else:
        #     model = "gpt-4"
        # if words_in_answer < 11:
        gpt_results, exception, in_tokens, out_tokens = gpt_process(
                session=session,
                answer_text=fixed_answer,
                answer_type=answer.experience_type,
                commerce_type=survey.commerce_type,
                model=model,
                drivers=drivers,
                logger=logger)
        if exception:
            error_text = "Error con GPT process." +\
                f"Error: {exception}. Respuesta GPT: {gpt_results}"
            logger.error(error_text)
            handle_error(session, answer, error_text, logger)
            return error_text
        # else:
        #     try:
        #         gpt_results, exceptions, in_tokens, out_tokens = split_process(
        #                 session=session,
        #                 answer_text=fixed_answer,
        #                 answer_type=answer.experience_type,
        #                 commerce_type=survey.commerce_type,
        #                 model=model,
        #                 drivers=drivers,
        #                 logger=logger)
        #     except Exception as e:
        #         error_text = "Error con split GPT process." +\
        #             f" Error: {e}."
        #         logger.error(error_text)
        #         handle_error(session, answer, error_text, logger)
        #         return error_text
        for driver_id in gpt_results:
            driver = None
            for obj in drivers:
                if obj.id == driver_id:
                    driver = obj
                    break
            for component_id in gpt_results[driver_id]:
                component = next(
                    obj for obj in driver.components if obj.id == component_id)
                component.gpt_result = gpt_results[driver_id][component_id]

    # Se guardan los resultados en la base de datos
    try:
        for driver in drivers:
            for component in driver.components:
                upsert_answer_component(
                    session=session,
                    component=component,
                    survey_id=survey.id,
                    driver_id=driver.id,
                    token=answer.token)
    except Exception as e:
        error_text = f"Error upserting answer_components. Error: {e}"
        logger.error(error_text)
        handle_error(session, answer, error_text, logger)
        return error_text

    # Se marca la respuesta como procesada
    try:
        answer.has_been_processed = True
        answer = update_answer(session=session, answer=answer)
        session.commit()
    except SQLAlchemyError as e:  # Captura errores específicos de SQLAlchemy
        logger.error(f"Error committing transaction. Error: {e}")
        session.rollback()
        return f"Error committing transaction. Error: {e}"

    logger.info(f"Respuesta con token {answer.token} procesada correctamente.")

    return answer


# Función separada para manejar errores
def handle_error(session, answer, error_text, logger):
    answer.did_have_an_error = True
    answer.has_been_processed = True
    insert_error_process(
        session=session,
        answer_token=answer.token,
        error_details=error_text,
        logger=logger)
    update_answer(session=session, answer=answer)
    session.flush()


def update_answer(session, answer):
    answer_data = {
        "token": answer.token,
        "answer": answer.answer_text,
        "did_have_an_error": answer.did_have_an_error,
        "has_been_processed": answer.has_been_processed,
        "experience": answer.experience_type
    }
    return upsert_answer(
        session=session,
        answer_data=answer_data,
        survey=answer.survey)
