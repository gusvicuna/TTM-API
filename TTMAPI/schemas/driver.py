from TTMAPI.models.driver import Driver


def driverSchema(item) -> dict:
    return {
        "name": item.name,
        "components": item.components
    }


def driversSchema(entity) -> list:
    return [driverSchema(Driver(**item)) for item in entity]
