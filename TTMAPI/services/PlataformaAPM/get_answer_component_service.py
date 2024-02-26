from sqlalchemy import text
from fastapi import HTTPException
from TTMAPI.models import AnswerComponent


def get_answer_component_service(
        session,
        token,
        component,
        driver,
        survey,
        logger) -> AnswerComponent:
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
    return answer_component
