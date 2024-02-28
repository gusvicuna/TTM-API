from TTMAPI.schemas.driver import (getMatchedDriversSchema)


def playgroundResponseSchema(
        driver: list,
        experience: str,
        input_tokens: int,
        output_tokens: int,
        model: str):
    if model == "gpt-4":
        k_token_value_input = 0.03
        k_token_value_output = 0.06
    elif model == "gpt-3.5-turbo":
        k_token_value_input = 0.0005
        k_token_value_output = 0.0015
    return {
        "experience": experience,
        "drivers": getMatchedDriversSchema(driver),
        "tokens": input_tokens + output_tokens,
        "price": round((input_tokens * k_token_value_input / 1000) +
                       (output_tokens * k_token_value_output / 1000), 4)
    }
