from TTMAPI.services.PlataformaAPM.get_answer_service import get_answer
from TTMAPI.services.PlataformaAPM.get_answer_component_service import (
    get_answer_component_service)


def get_processed_answer(token, session, logger):
    """
    Se obtiene la información de una respuesta procesada dado un token.
    El formato de respuesta está definido por el equipo de Plataforma APM.
    """
    results = {}
    results["token"] = token
    results["codificacion"] = []

    # Se obtiene la respuesta con el token
    answer = get_answer(session, token, logger)

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
        # Creamos los conjuntos de resultados de componentes para TTM y GPT,
        # y uno para guardar los componentes con prioridad en TTM
        gpt_component_result = []
        ttm_component_result = []
        priority_ttm_component_result = []
        for component in driver.components:
            component_result_gpt = {}
            component_result_ttm = {}
            component_result_priority_ttm = {}
            component_result_gpt["component_id"] = component.id
            component_result_ttm["component_id"] = component.id
            component_result_priority_ttm["component_id"] = component.id

            # Obtenemos la información de la respuesta del componente
            answer_component = get_answer_component_service(
                session, token, component, driver, survey, logger)

            # Polaridad de marca segun el tipo de respuesta:
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

            if answer_component.gpt_process != 0:
                component_result_gpt["resultado"] = resultado
            if answer_component.ttm_process != 0:
                component_result_ttm["resultado"] = resultado
            if component.ttm_priority:
                component_result_priority_ttm["resultado"] = resultado

            component_result_ttm["uts"] = []
            component_result_gpt["uts"] = []
            component_result_priority_ttm["uts"] = []

            # Se hace el mismo proceso para cada UT
            for ut in uts:
                ut_result = {}
                ut_result["ut_id"] = ut.id
                ut_result["components"] = []
                for ut_comp in ut.components:
                    ut_comp_result = {}
                    ut_comp_result["component_id"] = ut_comp.id
                    ut_answer_component = get_answer_component_service(
                        session, token, ut_comp, ut, survey, logger)

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
                    component_result_ttm["uts"].append(ut_result)
                    component_result_gpt["uts"].append(ut_result)
                    component_result_priority_ttm["uts"].append(ut_result)

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
                component_result_ttm["uts"].append(default_ut_driver)
                component_result_gpt["uts"].append(default_ut_driver)
                component_result_priority_ttm["uts"].append(default_ut_driver)

            # Si no hay componentes de UT, se agrega el default
            # (chequeamos el conjunto de TTM ya que es el mismo para ambos)
            if not component_result_ttm["uts"]:
                default_ut_driver = {}
                default_ut_component = {}
                default_ut_driver["ut_id"] = survey.default_ut_driver_id
                default_ut_driver["components"] = []
                default_ut_component["component_id"] =\
                    survey.default_ut_component_id
                default_ut_component["resultado"] = resultado
                default_ut_driver["components"].append(default_ut_component)
                component_result_ttm["uts"].append(default_ut_driver)
                component_result_gpt["uts"].append(default_ut_driver)
                component_result_priority_ttm["uts"].append(default_ut_driver)

            # Se agregan los resultados a los conjuntos de resultados
            if answer_component.gpt_process != 0:
                gpt_component_result.append(component_result_gpt)
            if answer_component.ttm_process != 0:
                ttm_component_result.append(component_result_ttm)
            if component.ttm_priority and answer_component.ttm_process != 0:
                priority_ttm_component_result.append(
                    component_result_priority_ttm)

        # Si tuvo marca de TTM y menos de 6 palabras,
        # se agrega el conjunto TTM
        if (len(answer.answer_text.split(" ")) < 6 and ttm_component_result):
            driver_result["components"] = ttm_component_result
            results["codificacion"].append(driver_result)
        # Sino, si tuvo marca de TTM y GPT,
        # se agrega el conjunto TTM
        elif (ttm_component_result and gpt_component_result):
            driver_result["components"] = ttm_component_result
            results["codificacion"].append(driver_result)
        # Sino, si el conjunto de ttm con prioridad no está vacío,
        # se agrega el conjunto con prioridad
        elif priority_ttm_component_result:
            driver_result["components"] = priority_ttm_component_result
            results["codificacion"].append(driver_result)
        # En caso contrario, no se guarda en la codificación

    # Si no tuvo ninguna codificación, se marca en duda
    if not results["codificacion"]:
        results["status"] = "en duda"
    logger.info(f"Answer: {answer.token} status: {results['status']}")
    return results
