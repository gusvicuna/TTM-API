from sqlalchemy.dialects.postgresql import insert
from TTMAPI.models.sqlalchemy_models import Answer


def upsert_answer(session, answer_data, survey):
    # Preparar el statement de inserción
    stmt = insert(Answer).values(
        token=answer_data["token"],
        answer_text=answer_data["answer"],
        survey_id=survey.id,
        experience_type=answer_data["experience"],
    )

    # Si ya existe un registro con el mismo token,
    # actualizamos el campo 'answer'
    if "has_been_processed" in answer_data and\
            "did_have_an_error" in answer_data:
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=['token'],
            set_=dict(
                answer_text=answer_data["answer"],
                has_been_processed=answer_data["has_been_processed"],
                did_have_an_error=answer_data["did_have_an_error"],
                )
        )

    else:
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=['token'],
            set_=dict(
                answer_text=answer_data["answer"],)
        )

    # Ejecutamos la instrucción
    session.execute(do_update_stmt)
    session.flush()

    # Recuperamos la respuesta actualizada
    # o la nueva respuesta creada para devolverla
    answer = session.query(Answer).filter_by(
        token=answer_data["token"]).first()

    return answer
