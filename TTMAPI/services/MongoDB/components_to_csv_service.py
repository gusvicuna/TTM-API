from TTMAPI.config.db import getMongo
from TTMAPI.models.driver import Driver


def drivers_and_components_to_csv_service(logger):
    """
    gets all drivers from the database,
    orders them by id,
    and writes them with their components,
    each with their aceptions, to a single csv file
    """
    db = getMongo()
    drivers_cursor = db["drivers"].find().sort("id", 1)
    drivers = []
    for driver in drivers_cursor:
        drivers.append(Driver(**driver))
    # order drivers by id
    drivers.sort(key=lambda x: x.id)
    with open("drivers_and_components.csv", "w") as f:
        f.write("driver_id;driver_name;component_id;component_name;phrase\n")
        for driver in drivers:
            driver_id = driver.id
            driver_name = driver.name
            driver_components = driver.components
            # order components by name
            driver_components.sort(key=lambda x: x.name)
            for component in driver_components:
                component_id = component.id
                component_name = component.name
                component_phrases = component.phrases
                # order phrases by name
                component_phrases.sort(key=lambda x: x)
                for phrase in component_phrases:
                    f.write(
                        f"{driver_id};{driver_name};" +
                        f"{component_id};{component_name};{phrase}\n"
                    )
    f.close()
    return True
