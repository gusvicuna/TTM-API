from TTMAPI.models.driver import Driver


def driverEntity(item) -> dict:
    return {
        "name": item.name,
        "components": item.components
    }


def driversEntity(entity) -> list:
    return [driverEntity(Driver(**item)) for item in entity]
