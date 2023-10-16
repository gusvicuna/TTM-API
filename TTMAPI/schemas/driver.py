from TTMAPI.models.driver import Driver
from TTMAPI.schemas.component import (
    createComponentSchema,
    createComponentsSchema,
    getComponentsSchema,
    getMatchedComponentsSchema,
    getComponentSchema,
    getMatchedComponentSchema)


def createDriverSchema(item: Driver) -> dict:
    return {
        "name": item.name,
        "driver_type": item.driver_type,
        "components": createComponentsSchema(item.components),
        "positives": createComponentSchema(item.positives),
        "negatives": createComponentSchema(item.negatives),
        "objects": createComponentSchema(item.objects)
    }


def getDriverSchema(item: Driver) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "driver_type": item.driver_type,
        "components": getComponentsSchema(item.components),
        "positives": getComponentSchema(item.positives),
        "negatives": getComponentSchema(item.negatives),
        "objects": getComponentSchema(item.objects)
    }


def getMatchedDriverSchema(item: Driver) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "driver_type": item.driver_type,
        "components": getMatchedComponentsSchema(item.components),
        "positives": getComponentSchema(item.positives),
        "negatives": getMatchedComponentSchema(item.negatives),
        "objects": getMatchedComponentSchema(item.objects)
    }


def getDriversSchema(entity) -> list:
    return [getDriverSchema(Driver(**item)) for item in entity]


def getMatchedDriversSchema(entity) -> list:
    return [getMatchedDriverSchema(item) for item in entity]
