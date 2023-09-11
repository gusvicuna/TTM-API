from sqlalchemy.dialects.postgresql import insert
from TTMAPI.models.sqlalchemy_models import Answer


def upsert_answer(session, answer_data, survey):
    # Preparar el statement de inserción
    stmt = insert(Answer).values(
        token=answer_data["token"],
        answer_text=answer_data["answer"],
        survey_id=survey.id
    )

    # Si ya existe un registro con el mismo token,
    # actualizamos el campo 'answer'
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=['token'],
        set_=dict(answer_text=answer_data["answer"])
    )

    # Ejecutamos la instrucción
    session.execute(do_update_stmt)
    session.flush()

    # Recuperamos la respuesta actualizada
    # o la nueva respuesta creada para devolverla
    answer = session.query(Answer).filter_by(
        token=answer_data["token"]).first()

    return answer
