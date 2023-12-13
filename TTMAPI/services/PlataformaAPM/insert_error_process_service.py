from sqlalchemy.dialects.postgresql import insert
from fastapi import HTTPException

from TTMAPI.models.sqlalchemy_models import ErrorProcess


def insert_error_process(session, error_details, answer_token, logger):
    try:
        # Preparar el statement de inserción
        stmt = insert(ErrorProcess).values(
            answer_token=answer_token,
            error_details=error_details
        )

        # Ejecutamos la instrucción
        session.execute(stmt)
        session.flush()
        logger.info("Error_process created")
    except Exception as e:
        logger.error(f"Error inserting error process: {e}")
        raise HTTPException(status_code=502, detail=e)

    session.commit()

    return
