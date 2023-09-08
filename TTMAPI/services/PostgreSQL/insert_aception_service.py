from fastapi import HTTPException
from TTMAPI.models.sqlalchemy_models import Aception


def insert_aception(session, phrase, component, logger):
    try:
        aception = Aception(
            phrase=phrase,
            component=component)
        session.add(aception)
        session.flush()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    return aception
