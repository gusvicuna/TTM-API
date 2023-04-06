from TTMAPI.models.driver import Driver
from TTMAPI.schemas.component import componentsSchema, matchedComponentsSchema


def driverSchema(item) -> dict:
    return {
        "name": item.name,
        "components": componentsSchema(item.components)
    }


def matchedDriverSchema(item) -> dict:
    return {
        "name": item.name,
        "components": matchedComponentsSchema(item.components)
    }


def driversSchema(entity) -> list:
    return [driverSchema(Driver(**item)) for item in entity]


def matchedDriversSchema(entity) -> list:
    return [matchedDriverSchema(item) for item in entity]
