from fastapi import HTTPException
from TTMAPI.models.sqlalchemy_models import Answer, AnswerComponent


def get_processed_answer(token, session, logger):
    results = {}
    results["token"] = token
    results["codificacion"] = []
    answer = session.query(Answer).filter_by(
        token=token).first()
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
            component_result = {}
            component_result["component_id"] = component.id
            try:
                answer_component = session.query(AnswerComponent).filter_by(
                    answer_token=token,
                    component_id=component.id
                ).first()
            except Exception as e:
                logger.error(f"AnswerComponent not found. Error: {e}")
                raise HTTPException(status_code=500, detail=e)

            if answer_component.ttm_process != 0:
                resultado = answer_component.ttm_process
            else:
                resultado = answer_component.gpt_process
            component_result["resultado"] = resultado

            # TODO: Modificar luego de arreglar codificación con UTs
            component_result["ut"] = []
            if resultado != 0:
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
                        ut_comp_result["resultado"] =\
                            ut_answer_component.gpt_process
                        ut_result["components"].append(ut_comp_result)
                    component_result["ut"].append(ut_result)

            driver_result["components"].append(component_result)
        results["codificacion"].append(driver_result)

    return results
