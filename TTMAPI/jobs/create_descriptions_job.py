from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.models.sqlalchemy_models import Survey
from TTMAPI.services.OpenAI.generate_description import generate_description


logger = get_logger(__name__)


def create_descriptions():
    session = getPostgreSQL()

    try:
        survey = session.query(Survey).filter_by(
            has_been_described=False).first()
    except Exception as e:
        logger.error(f"Hubo un error obteniendo la encuesta. Error: {e}")
        return e

    if not survey:
        logger.info("No se encuentran encuestas sin describir")
        return "No se encuentran encuestas sin describir"

    for driver in survey.drivers:
        for component in driver.components:
            phrases = []
            for aception in component.aceptions:
                phrases.append(aception.phrase)
            component.description = generate_description(
                name=component.name,
                phrases=phrases,
                logger=logger)

    survey.has_been_described = True
    session.commit()
    session.close()

    return survey
