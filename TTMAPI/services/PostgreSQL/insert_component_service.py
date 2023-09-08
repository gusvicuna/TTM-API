from fastapi import HTTPException
from TTMAPI.models.sqlalchemy_models import Component


def insert_component(session, component_data, driver, logger):
    try:
        component = Component(name=component_data["name"], driver=driver)
        session.add(component)
        session.flush()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    return component
