import openai
import json
from dotenv import dotenv_values
from fastapi import HTTPException

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def gpt_simple_process(traintext: str, drivers, logger):
    components_result = {}
    for driver in drivers:
        for component in driver.components:
            components_result[component.name] = 0

    prompt_instruction = "TTMAPI/services/OpenAI/prompt_instruction_simple.txt"

    try:

        with open(prompt_instruction, 'r') as file:
            prompt_instruction: str = file.read()

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_instruction},
                {"role": "user", "content": traintext}],
            temperature=0.2,
            max_tokens=814,
            top_p=0.4,
            frequency_penalty=0,
            presence_penalty=0
        )
        result = response['choices'][0]['message']['content']

        logger.info(f"gptresponse: {result}")

        json_result = json.loads(result)
        for key in json_result:
            if key in components_result:
                components_result[key] = json_result[key]
        return components_result
    except Exception as e:
        logger.error(f"{e}, GPT: {result}")
        raise HTTPException(status_code=502, detail="Bad response from GPT")
