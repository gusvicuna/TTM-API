from TTMAPI.models.driver import Driver

from .get_all_driver_service import get_all_drivers_service
from .get_driver_by_id_service import get_driver_by_id_service
from .create_new_driver_service import create_new_driver_service
from .update_driver_service import update_driver_service


def get_all_drivers(logger):
    return get_all_drivers_service(logger=logger)


def get_driver_by_id(name: str, logger):
    return get_driver_by_id_service(name=name, logger=logger)


def create_new_driver(driver: Driver, logger):
    return create_new_driver_service(driver=driver, logger=logger)


def update_driver(driver: Driver, name: str, logger):
    return update_driver_service(driver=driver, name=name, logger=logger)
