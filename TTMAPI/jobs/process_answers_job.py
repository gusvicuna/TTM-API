from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.services.PostgreSQL.process_answer_service import process_answer


logger = get_logger(__name__)


def process_answers():
    session = getPostgreSQL()
    logger.info("Buscando respuestas disponibles para procesar.")
    process_answer(session=session, logger=logger)
    session.close()
