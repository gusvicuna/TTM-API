from openai import OpenAI
from dotenv import dotenv_values

from TTMAPI.services.Playground import get_prompt

config = dotenv_values("settings.env")

api_key = config["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)


def fix_grammar(
        originalText: str,
        convertToChilean: bool,
        session,
        logger):
    logger.debug(f"fixing grammar of: {originalText}")
    prompt = get_prompt(
        session=session,
        prompt_id=3,
        logger=logger)
    prompt_modifiable_instruction = prompt.modifiable_instruction
    prompt_unmodifiable_instruction = prompt.unmodifiable_instruction

    system_instruction = prompt_unmodifiable_instruction
    if convertToChilean:
        system_instruction += prompt_modifiable_instruction

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_instruction
            },
            {
                "role": "user",
                "content": originalText
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    logger.debug(completion.choices[0].message.content)
    return completion.choices[0].message.content
