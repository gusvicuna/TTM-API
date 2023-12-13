from TTMAPI.models.sqlalchemy_models import Driver
from sqlalchemy.dialects.postgresql import insert


def upsert_driver(session, driver_data, survey):
    # Preparar el statement de inserción
    stmt = insert(Driver).values(
        id=driver_data["id"],
        name=driver_data["name"],
        type=driver_data["type"],
        survey_id=survey.id,
        default_ut_driver_id=driver_data["default_ut"]["driver_id"],
        default_ut_component_id=driver_data["default_ut"]["ut_id"]
    )

    # Si ya existe un registro con el mismo id y survey_id,
    # actualizamos los datos relevantes
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=['id', 'survey_id'],
        set_=dict(
            name=driver_data["name"],
            type=driver_data["type"],
            default_ut_driver_id=driver_data["default_ut"]["driver_id"],
            default_ut_component_id=driver_data["default_ut"]["ut_id"]
            )
    )

    # Ejecutamos la instrucción
    session.execute(do_update_stmt)
    session.flush()

    # Obtenemos el driver actualizado o el nuevo driver creado para retornarlo
    driver = session.query(Driver).filter(
        Driver.id == driver_data["id"],
        Driver.survey_id == survey.id
    ).first()

    return driver
