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
        "positives": componentSchema(item.positives),
        "negatives": componentSchema(item.negatives),
        "objects": componentSchema(item.objects)
    }


def matchedDriverSchema(item: Driver) -> dict:
    return {
        "dbid": item.dbid,
        "name": item.name,
        "components": matchedComponentsSchema(item.components),
        "positives": componentSchema(item.positives),
        "negatives": matchedComponentSchema(item.negatives),
        "objects": matchedComponentSchema(item.objects)
    }


def driversSchema(entity) -> list:
    return [driverSchema(Driver(**item)) for item in entity]


def matchedDriversSchema(entity) -> list:
    return [matchedDriverSchema(item) for item in entity]
