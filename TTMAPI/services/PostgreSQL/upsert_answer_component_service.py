from sqlalchemy.dialects.postgresql import insert
from fastapi import HTTPException

from TTMAPI.models.sqlalchemy_models import AnswerComponent


def upsert_answer_component(session, component, survey_id, driver_id, token):
    try:
        # Preparar el statement de inserción
        stmt = insert(AnswerComponent).values(
            answer_token=token,
            component_id=component.id,
            driver_id=driver_id,
            survey_id=survey_id,
            gpt_process=component.gpt_result,
            ttm_process=component.ttm_result
        )

        # Si ya existe un registro con la misma combinación,
        # simplemente evitamos el error de duplicación
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=[
                'answer_token',
                'component_id',
                'driver_id',
                'survey_id'],
            set_=dict(
                gpt_process=component.gpt_result,
                ttm_process=component.ttm_result)
        )

        # Ejecutamos la instrucción
        session.execute(do_update_stmt)
        session.flush()
    except Exception as e:
        raise HTTPException(status_code=502, detail=e)

    session.commit()

    # Obtenemos la answer_component actualizada
    # o la nueva answer_component creada para retornarla
    answer_component = session.query(AnswerComponent).filter(
        AnswerComponent.answer_token == token,
        AnswerComponent.component_id == component.id,
        AnswerComponent.driver_id == driver_id,
        AnswerComponent.survey_id == survey_id
    ).first()

    return answer_component
