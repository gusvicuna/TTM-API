from TTMAPI.models.sqlalchemy_models import Component
from sqlalchemy.dialects.postgresql import insert


def upsert_component(session, component_data, component_type, driver, logger):
    # Preparar el statement de inserción
    stmt = insert(Component).values(
        id=component_data["id"],
        name=component_data["name"],
        description=component_data["description"],
        type=component_type,
        ttm_priority=component_data["ttm_priority"],
        has_manual_desc=bool(component_data["description"]),
        driver_id=driver.id,
        survey_id=driver.survey_id
    )

    # Si ya existe un registro con el mismo id, driver_id y survey_id,
    # actualizamos los datos relevantes
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=['id', 'driver_id', 'survey_id'],
        set_=dict(
            name=component_data["name"],
            description=component_data["description"],
            type=component_type,
            ttm_priority=component_data["ttm_priority"],
            has_manual_desc=bool(component_data["description"]),
            )
    )

    # Ejecutamos la instrucción
    session.execute(do_update_stmt)
    session.flush()

    # Obtenemos el componente actualizado
    # o el nuevo componente creado para retornarlo
    component = session.query(Component).filter(
        Component.id == component_data["id"],
        Component.driver_id == driver.id,
        Component.survey_id == driver.survey_id
    ).first()

    return component
