from fastapi import HTTPException
from sqlalchemy import text
from TTMAPI.models.sqlalchemy_models import Answer, AnswerComponent


def get_processed_answer(token, session, logger):
    """
    Se obtiene la información de una respuesta procesada dado un token.
    El formato de respuesta está definido por el equipo de Plataforma APM.
    """
    results = {}
    results["token"] = token
    results["codificacion"] = []

    # Se obtiene la respuesta con el token
    try:
        answer = session.query(Answer).filter_by(
            token=token).first()
    except Exception as e:
        logger.error(f"Error intentando obtener respuesta. Error: {e}")
        raise HTTPException(status_code=500, detail=e)
    if not answer:
        logger.error(f"Respuesta con token {token} no encontrada")
        results["status"] = "not found"
        return results

    # Se verifica si la respuesta fue procesada y si tuvo errores
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

    # Guardamos los uts primero para iterar luego..
    uts = []
    for driver in survey.drivers:
        if driver.type == "ut":
            uts.append(driver)

    # Iteramos por cada driver
    for driver in survey.drivers:
        if driver.type == "ut":
            continue
        driver_result = {}
        driver_result["driver_id"] = driver.id
        driver_result["components"] = []
        did_have_gpt_mark = False
        did_have_ttm_mark = False
        for component in driver.components:
            try:
                answer_component_result = session.execute(
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
            except Exception as e:
                logger.error(f"Error obteniendo AnswerComponent. Error: {e}")
                raise HTTPException(status_code=500, detail=e)
            if not answer_component_result:
                logger.error("AnswerComponent no encontrada.")
                raise HTTPException(status_code=500,
                                    detail="AnswerComponent not found.")

            answer_component_data = {
                    'answer_token': answer_component_result[0],
                    'component_id': answer_component_result[1],
                    'driver_id': answer_component_result[2],
                    'survey_id': answer_component_result[3],
                    'gpt_process': answer_component_result[4],
                    'ttm_process': answer_component_result[5]
                }
            answer_component = AnswerComponent(**answer_component_data)

            if answer_component.gpt_process != 0:
                did_have_gpt_mark = True
            if answer_component.ttm_process != 0:
                did_have_ttm_mark = True

            # Filtro de resultados segun el resultado de cada proceso:
            # Si la respuesta es de tipo Muy Buena, se marca positivo siempre,
            # al menos que ambas respuestas sean -1
            if answer.experience_type == "MB":
                if answer_component.ttm_process == -1 and\
                        answer_component.gpt_process == -1:
                    resultado = -1
                elif answer_component.ttm_process != 0 or\
                        answer_component.gpt_process != 0:
                    resultado = 1
                else:
                    resultado = 0
            # Si la respuesta es de tipo Mala, se marca negativo siempre,
            # al menos que ambas respuestas sean 1
            elif answer.experience_type == "M":
                if answer_component.ttm_process == 1 and\
                        answer_component.gpt_process == 1:
                    resultado = 1
                elif answer_component.ttm_process != 0 or\
                        answer_component.gpt_process != 0:
                    resultado = -1
                else:
                    resultado = 0
            # Si la respuesta es de tipo Buena, se marca negativo
            elif answer.experience_type == "B":
                if answer_component.ttm_process != 0 or\
                        answer_component.gpt_process != 0:
                    resultado = -1
                else:
                    resultado = 0

            if resultado == 0:
                continue

            component_result = {}
            component_result["component_id"] = answer_component.component_id
            component_result["resultado"] = resultado
            component_result["uts"] = []

            # Se hace el mismo proceso para cada UT
            for ut in uts:
                ut_result = {}
                ut_result["ut_id"] = ut.id
                ut_result["components"] = []
                for ut_comp in ut.components:
                    ut_comp_result = {}
                    ut_comp_result["component_id"] = ut_comp.id

                    try:
                        answer_component_result = session.execute(
                            text("SELECT * FROM answer_components" +
                                 " WHERE answer_token = :token" +
                                 " AND component_id = :component_id" +
                                 " AND driver_id = :driver_id" +
                                 " AND survey_id = :survey_id"),
                            {
                                "token": token,
                                "component_id": ut_comp.id,
                                "driver_id": ut.id,
                                "survey_id": survey.id}
                        ).fetchone()
                    except Exception as e:
                        logger.error(
                            f"Error getting UTAnswerComponent. Error: {e}")
                        raise HTTPException(status_code=500, detail=e) from e
                    if not answer_component_result:
                        logger.error("UTAnswerComponent not found.")
                        raise HTTPException(
                            status_code=500,
                            detail="UTAnswerComponent not found.")

                    answer_component_data = {
                            'answer_token': answer_component_result[0],
                            'component_id': answer_component_result[1],
                            'driver_id': answer_component_result[2],
                            'survey_id': answer_component_result[3],
                            'gpt_process': answer_component_result[4],
                            'ttm_process': answer_component_result[5]
                        }
                    ut_answer_component = AnswerComponent(
                        **answer_component_data)

                    if answer.experience_type == "MB":
                        if ut_answer_component.ttm_process == -1 and\
                                ut_answer_component.gpt_process == -1:
                            ut_comp_result["resultado"] = -1
                        elif ut_answer_component.ttm_process != 0 or\
                                ut_answer_component.gpt_process != 0:
                            ut_comp_result["resultado"] = 1
                        else:
                            ut_comp_result["resultado"] = 0
                    elif answer.experience_type == "M":
                        if ut_answer_component.ttm_process == 1 and\
                                ut_answer_component.gpt_process == 1:
                            ut_comp_result["resultado"] = 1
                        elif ut_answer_component.ttm_process != 0 or\
                                ut_answer_component.gpt_process != 0:
                            ut_comp_result["resultado"] = -1
                        else:
                            ut_comp_result["resultado"] = 0
                    elif answer.experience_type == "B":
                        if ut_answer_component.ttm_process != 0 or\
                                ut_answer_component.gpt_process != 0:
                            ut_comp_result["resultado"] = -1
                        else:
                            ut_comp_result["resultado"] = 0

                    if ut_comp_result["resultado"] != 0:
                        ut_result["components"].append(ut_comp_result)

                if ut_result["components"]:
                    component_result["uts"].append(ut_result)

            # Si existe un componente ut default en el driver, se guarda en el
            # resultado
            if driver.default_ut_driver_id:
                default_ut_driver = {}
                default_ut_driver["ut_id"] = driver.default_ut_driver_id
                default_ut_driver["components"] = []
                default_ut_component = {}
                default_ut_component["component_id"] =\
                    driver.default_ut_component_id
                default_ut_component["resultado"] = resultado
                default_ut_driver["components"].append(default_ut_component)
                component_result["uts"].append(default_ut_driver)

            # Si no hay componentes de UT, se agrega el default
            if not component_result["uts"]:
                default_ut_driver = {}
                default_ut_component = {}
                default_ut_driver["ut_id"] = survey.default_ut_driver_id
                default_ut_driver["components"] = []
                default_ut_component["component_id"] =\
                    survey.default_ut_component_id
                default_ut_component["resultado"] = resultado
                default_ut_driver["components"].append(default_ut_component)
                component_result["uts"].append(default_ut_driver)

            driver_result["components"].append(component_result)

        # Si tuvo marca de TTM y GPT, se agrega a la codificación
        if (did_have_ttm_mark and did_have_gpt_mark):
            results["codificacion"].append(driver_result)
        # Si no tuvo marca de TTM o GPT, se agrega a la codificación si
        # la respuesta es corta
        elif (len(answer.answer_text.split(" ")) < 6 and
                driver_result["components"]):
            results["codificacion"].append(driver_result)
        # En caso contrario, no se guarda en la codificación

    # Si no tuvo ninguna codificación, se marca en duda
    if not results["codificacion"]:
        results["status"] = "en duda"
    logger.info(f"Answer: {answer.token} status: {results['status']}")
    return results
