from TTMAPI.models.driver import Driver

from .get_all_driver_service import get_all_drivers_service
from .get_driver_by_id_service import get_driver_by_id_service
from .create_new_driver_service import create_new_driver_service
from .update_driver_service import update_driver_service
from .delete_driver_service import delete_driver_service


def get_all_drivers(logger):
    return get_all_drivers_service(logger=logger)


def get_driver_by_id(driver_id: int, logger):
    return get_driver_by_id_service(driver_id=driver_id, logger=logger)


def create_new_driver(driver: Driver, logger):
    return create_new_driver_service(driver=driver, logger=logger)


def update_driver(driver: Driver, driver_id: int, logger):
    return update_driver_service(
        driver=driver,
        driver_id=driver_id,
        logger=logger)


def delete_driver(driver_id: int, logger):
    return delete_driver_service(driver_id=driver_id, logger=logger)