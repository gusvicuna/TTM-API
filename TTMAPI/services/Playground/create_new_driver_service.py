from TTMAPI.config.db import getMongo
from TTMAPI.models.driver import Driver
from fastapi import HTTPException


def create_new_driver_service(driver: Driver, logger):
    db = getMongo()
    try:
        # Obtener el siguiente ID autoincrementado para el driver
        driver["id"] = get_next_sequence("driver_id")

        # Asignar IDs a los componentes en la lista "components"
        for component in driver["components"]:
            component["id"] = get_next_sequence("component_id")

        # Asignar IDs a "objects", "positives" y "negatives"
        driver["objects"]["id"] = get_next_sequence("component_id")
        driver["positives"]["id"] = get_next_sequence("component_id")
        driver["negatives"]["id"] = get_next_sequence("component_id")

        # Insertar el driver en la base de datos
        db["drivers"].insert_one(driver)

        # Resetear el contador de componentes
        reset_component_counter()

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def get_next_sequence(name):
    db = getMongo()
    return db["counters"].find_one_and_update(
        {"_id": name},
        {"$inc": {"seq": 1}},
        return_document=True
    )["seq"]


def reset_component_counter():
    db = getMongo()
    db["counters"].update_one({"_id": "component_id"}, {"$set": {"seq": 0}})
