from fastapi import HTTPException
from sqlalchemy import text
from TTMAPI.models.sqlalchemy_models import Answer, AnswerComponent


def get_processed_answer(token, session, logger):
    results = {}
    results["token"] = token
    results["codificacion"] = []

    try:
        answer = session.query(Answer).filter_by(
            token=token).first()
    except Exception as e:
        logger.error(f"Error trying to get answer. Error: {e}")
        raise HTTPException(status_code=500, detail=e)

    if not answer:
        logger.error(f"Answer {token} not found")
        results["status"] = "not found"
        return results

    if answer.has_been_processed:
        if answer.did_have_an_error:
            results["status"] = "error"
            return results
        else:
            results["status"] = "procesado"
    else:
        results["status"] = "en cola"
        return results

    survey = answer.survey

    uts = []
    for driver in survey.drivers:
        if driver.type == "ut":
            uts.append(driver)

    for driver in survey.drivers:
        if driver.type == "ut":
            continue
        driver_result = {}
        driver_result["driver_id"] = driver.id
        driver_result["components"] = []
        for component in driver.components:
            try:
                result = session.execute(
                    text("SELECT * FROM answer_components" +
                         " WHERE answer_token = :token" +
                         " AND component_id = :component_id" +
                         " AND driver_id = :driver_id" +
                         " AND survey_id = :survey_id"),
                    {
                        "token": token,
                        "component_id": component.id,
                        "driver_id": driver.id,
                        "survey_id": survey.id}
                ).fetchone()

                if result:
                    answer_component_data = {
                        'answer_token': result[0],
                        'component_id': result[1],
                        'driver_id': result[2],
                        'survey_id': result[3],
                        'gpt_process': result[4],
                        'ttm_process': result[5]
                    }
                    answer_component = AnswerComponent(**answer_component_data)
                else:
                    print("Direct query found nothing.")

            except Exception as e:
                logger.error(f"Error getting answerComponent. Error: {e}")
                raise HTTPException(status_code=500, detail=e)

            if not answer_component:
                logger.error("AnswerComponent not found.")
                raise HTTPException(status_code=500,
                                    detail="AnswerComponent not found.")

            if answer_component.ttm_process != 0:
                resultado = answer_component.ttm_process
            else:
                resultado = answer_component.gpt_process
            if resultado == 0:
                continue

            component_result = {}
            component_result["component_id"] = answer_component.component_id
            component_result["resultado"] = resultado
            component_result["ut"] = []
            # TODO: Modificar luego de arreglar codificación con UTs
            for ut in uts:
                ut_result = {}
                ut_result["ut_id"] = ut.id
                ut_result["components"] = []
                for ut_comp in ut.components:
                    ut_comp_result = {}
                    ut_comp_result["component_id"] = ut_comp.id
                    try:
                        ut_answer_component =\
                            session.query(AnswerComponent).filter_by(
                                answer_token=token,
                                component_id=ut_comp.id).first()
                    except Exception as e:
                        logger.error(
                            f"AnswerComponent not found. Error: {e}")
                        raise HTTPException(status_code=500, detail=e)
                    if ut_answer_component.ttm_process != 0:
                        ut_comp_result["resultado"] =\
                            answer_component.ttm_process
                    else:
                        ut_comp_result["resultado"] =\
                            answer_component.gpt_process
                    # if ut_comp_result["resultado"] != 0:
                        ut_result["components"].append(ut_comp_result)
                component_result["ut"].append(ut_result)

            driver_result["components"].append(component_result)
        results["codificacion"].append(driver_result)

    return results
