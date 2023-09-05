from TTMAPI.models.sqlalchemy_models import Component


def insert_component(session, component_data, driver):
    component = Component(name=component_data["name"], driver=driver)
    session.add(component)
    session.flush()
    return component
