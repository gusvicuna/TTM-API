from openai import OpenAI
from dotenv import dotenv_values

from TTMAPI.services.Playground import get_prompt

config = dotenv_values("settings.env")

api_key = config["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)


def generate_description(session, name, phrases, logger):

    prompt = get_prompt(
        session=session,
        prompt_id=2,
        logger=logger)
    prompt_modifiable_instruction = prompt.modifiable_instruction
    prompt_unmodifiable_instruction = prompt.unmodifiable_instruction

    prompt_instruction = prompt_modifiable_instruction +\
        "\n" + prompt_unmodifiable_instruction

    component = {}
    component["name"] = name
    component["phrases"] = phrases

    logger.info(f"Component: {component['name']}")

    try:
        completion = client.chat.completions.create(
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
        result = completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error with GPT: {e}")
        raise e

    logger.info(f"gptresponse: {result}")
    return result
