from TTMAPI.models.sqlalchemy_models import Driver


def insert_driver(session, driver_data, survey, driver_type):
    name = driver_type
    if (driver_type == "driver"):
        name = "drivers"
    driver = Driver(
        name=driver_data[name],
        type=driver_type,
        survey=survey)
    session.add(driver)
    session.flush()
    return driver
