from TTMAPI.schemas.driver import (getMatchedDriversSchema)


def getProcessedExperienceSchema(driver: list, experience: str):
    return {
        "experience": experience,
        "drivers": getMatchedDriversSchema(driver)
    }
