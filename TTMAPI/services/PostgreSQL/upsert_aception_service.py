from sqlalchemy.dialects.postgresql import insert

from TTMAPI.models.sqlalchemy_models import Aception


def upsert_aception(session, phrase, component):
    # Preparar el statement de inserción
    stmt = insert(Aception).values(
        phrase=phrase,
        component_id=component.id,
        driver_id=component.driver_id,
        survey_id=component.survey_id
    )

    # Si ya existe un registro con la misma combinación de phrase y IDs,
    # simplemente evitamos el error de duplicación
    do_nothing_stmt = stmt.on_conflict_do_nothing(
        index_elements=['phrase', 'component_id', 'driver_id', 'survey_id']
    )

    # Ejecutamos la instrucción
    session.execute(do_nothing_stmt)
    session.flush()

    # Obtenemos la aception actualizada
    # o la nueva aception creada para retornarla
    aception = session.query(Aception).filter(
        Aception.phrase == phrase,
        Aception.component_id == component.id,
        Aception.driver_id == component.driver_id,
        Aception.survey_id == component.survey_id
    ).first()

    return aception
