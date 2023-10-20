import openai
from dotenv import dotenv_values

from TTMAPI.models.prompt import Prompt
from TTMAPI.services.MongoDB import get_prompt

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def generate_description(name, phrases, logger):

    prompt_cursor = get_prompt(prompt_id=2, logger=logger)
    prompt = Prompt(**prompt_cursor)
    prompt_modifiable_instruction = prompt.modifiable_instruction
    prompt_unmodifiable_instruction = prompt.unmodifiable_instruction

    prompt_instruction = prompt_modifiable_instruction +\
        "\n" + prompt_unmodifiable_instruction

    logger.debug(f"Prompt: {prompt_instruction}")

    component = {}
    component["name"] = name
    component["phrases"] = phrases

    logger.debug(f"Component: {component['name']}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_instruction},
                {"role": "user", "content": str(component)}],
            temperature=0.2,
            max_tokens=814,
            top_p=0.4,
            frequency_penalty=0,
            presence_penalty=0
        )
        result = response['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Error with GPT: {e}")
        raise e

    logger.info(f"gptresponse: {result}")
    return result
