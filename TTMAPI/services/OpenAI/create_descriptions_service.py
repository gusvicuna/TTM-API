from TTMAPI.models.sqlalchemy_models import Survey
from TTMAPI.services.OpenAI.generate_description import generate_description


def create_descriptions(session, logger):
    try:
        survey = session.query(Survey).filter_by(
            has_been_described=False,
            did_have_an_error=False).first()
    except Exception as e:
        logger.error(f"Hubo un error obteniendo la encuesta. Error: {e}")
        return e

    if not survey:
        logger.info("No se encuentran encuestas sin describir")
        return "No se encuentran encuestas sin describir"

    try:
        for driver in survey.drivers:
            for component in driver.components:
                phrases = []
                for aception in component.aceptions:
                    phrases.append(aception.phrase)
                component.description = generate_description(
                    name=component.name,
                    phrases=phrases,
                    logger=logger)

        logger.info("Finished creating descriptions.")
        survey.has_been_described = True
        session.commit()
    except Exception as e:
        logger.error(f"Error: {e}")
        survey.did_have_an_error = True
        session.commit()

    return survey
