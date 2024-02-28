from TTMAPI.schemas.driver import (getMatchedDriversSchema)


def playgroundResponseSchema(driver: list, experience: str, tokens: int):
    return {
        "experience": experience,
        "drivers": getMatchedDriversSchema(driver),
        "tokens": tokens
    }
