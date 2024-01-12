from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.services.OpenAIServices.create_descriptions_service import (
    create_descriptions as cd)


logger = get_logger(__name__)


def create_descriptions():
    session = getPostgreSQL()

    logger.info("Executing create_descriptions job")
    result = None
    try:
        result = cd(session=session, logger=logger)
    finally:
        session.close()

    return result
