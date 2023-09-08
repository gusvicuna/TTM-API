from fastapi import HTTPException, status
from sqlalchemy.dialects.postgresql import insert

from TTMAPI.models.sqlalchemy_models import Survey


def upsert_survey(session, survey_data, logger):
    try:
        # Preparar el statement de inserción
        stmt = insert(Survey).values(
            description=survey_data["description"],
            id=survey_data["id"]
        )

        # Si ya existe un registro con el mismo id, actualizamos la descripción
        do_update_stmt = stmt.on_conflict_do_update(
            index_elements=['id'],
            set_=dict(description=survey_data["description"])
        )

        # Ejecutamos la instrucción
        session.execute(do_update_stmt)
        session.flush()

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))

    survey = session.query(Survey).filter_by(id=survey_data["id"]).first()
    return survey
