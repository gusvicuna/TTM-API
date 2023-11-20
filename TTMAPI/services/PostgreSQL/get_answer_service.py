from sqlalchemy.dialects.postgresql import insert
from TTMAPI.models.sqlalchemy_models import Answer


def get_answer(session, tokene, logger):
    try:
        answer = session.query(Answer).filter_by(
            token=token).first()
    except Exception as e:
        session.rollback()
        logger.error(f"Error obteniendo respuesta. Error: {e}")
        raise e
    return answer
