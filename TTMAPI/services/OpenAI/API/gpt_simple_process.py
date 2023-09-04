import openai
import json
from dotenv import dotenv_values
from fastapi import HTTPException

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def gpt_simple_process(traintext: str, drivers, logger):
    components = {}
    uts = {}
    for driver in drivers:
        if not driver.isUT:
            for component in driver.components:
                components[component.name] = component.description
        else:
            for component in driver.components:
                uts[component.name] = component.description

    prompt_instruction_file = "TTMAPI/services/OpenAI/" +\
        "prompt_instruction_simple.txt"
    with open(prompt_instruction_file, 'r') as file:
        prompt_instruction: str = file.read()

    system_instruction = prompt_instruction +\
        f"\nComponentes:\n{components}\nUnidades Tácticas:\n{uts}"
    print(system_instruction)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_instruction},
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
    except Exception as e:
        logger.error(f"{e}, GPT: {result}")
        raise HTTPException(status_code=502, detail="Bad response from GPT")

    results = {}
    for driver in drivers:
        for component in driver.components:
            results[component.name] = 0
    for key in json_result:
        if key in results:
            results[key] = json_result[key]
    return results
