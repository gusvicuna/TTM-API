from TTMAPI.models.driver import Driver
from TTMAPI.schemas.component import (
    componentsSchema,
    matchedComponentsSchema,
    componentSchema,
    matchedComponentSchema)


def driverSchema(item: Driver) -> dict:
    return {
        "dbid": item.dbid,
        "name": item.name,
        "components": componentsSchema(item.components),
        "negatives": componentSchema(item.negatives),
        "isItPositive": item.isPositive
    }


def matchedDriverSchema(item: Driver) -> dict:
    return {
        "dbid": item.dbid,
        "name": item.name,
        "components": matchedComponentsSchema(item.components),
        "negatives": matchedComponentSchema(item.negatives),
        "isItPositive": item.isPositive
    }


def driversSchema(entity) -> list:
    return [driverSchema(Driver(**item)) for item in entity]


def matchedDriversSchema(entity) -> list:
    return [matchedDriverSchema(item) for item in entity]
