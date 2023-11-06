from sqlalchemy.dialects.postgresql import insert

from TTMAPI.models.sqlalchemy_models import Survey


def upsert_survey(session, survey_data):
    # Preparar el statement de inserción
    stmt = insert(Survey).values(
        id=survey_data["id"],
        description=survey_data["description"],
        default_ut_driver_id=survey_data["default_ut"]["driver_id"],
        default_ut_component_id=survey_data["default_ut"]["ut_id"],
    )

    # Si ya existe un registro con el mismo id, actualizamos los campos
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=['id'],
        set_={
            "description": survey_data["description"],
            "default_ut_driver_id": survey_data["default_ut"]["driver_id"],
            "default_ut_component_id": survey_data["default_ut"]["ut_id"]
            }
    )

    # Ejecutamos la instrucción
    session.execute(do_update_stmt)
    session.flush()
    survey = session.query(Survey).filter_by(id=survey_data["id"]).first()
    return survey
