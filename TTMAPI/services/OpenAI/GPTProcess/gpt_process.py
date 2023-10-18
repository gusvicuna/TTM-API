import openai
import json
from dotenv import dotenv_values
from fastapi import HTTPException

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def create_empty_results(drivers):
    results = {}
    for driver in drivers:
        results[driver.id] = {}
        for component in driver.components:
            results[driver.id][component.id] = 0
    return results


def gpt_process(answer: str, drivers, logger):
    components = {}
    uts = {}
    for driver in drivers:
        if driver.driver_type == "driver":
            components[driver.id] = {}
            for component in driver.components:
                components[driver.id][component.id] = {
                    "name": component.name,
                    "description": component.description
                }
        elif driver.driver_type == "ut":
            uts[driver.id] = {}
            for component in driver.components:
                uts[driver.id][component.id] = {
                    "name": component.name,
                    "description": component.description
                }

    prompt_instruction_file = "TTMAPI/services/OpenAI/" +\
        "GPTProcess/gpt_process_prompt.txt"
    prompt_example_file = "TTMAPI/services/OpenAI/" +\
        "GPTProcess/gpt_process_example.txt"

    with open(prompt_instruction_file, 'r', encoding='utf-8') as file:
        prompt_instruction: str = file.read()
    with open(prompt_example_file, 'r', encoding='utf-8') as file:
        prompt_example: str = file.read()
    prompt_instruction += "\n" + prompt_example

    system_instruction = prompt_instruction +\
        f"\nComponentes:\n{components}\nUnidades Tácticas:\n{uts}"

    user_experience = "Procesa la siguiente experiencia: " + answer

    results = create_empty_results(drivers)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_experience}],
            temperature=0.2,
            max_tokens=814,
            top_p=0.4,
            frequency_penalty=0,
            presence_penalty=0
        )
        result = response['choices'][0]['message']['content']

        logger.info(f"gptresponse: {result}")

        try:
            json_result = json.loads(result)
        except json.JSONDecodeError:
            logger.error(f"JSON Decode Error for result: {result}")
            raise HTTPException(
                status_code=502, detail="Bad JSON format in GPT response")

    except Exception as e:
        logger.error(f"General Error: {e}, GPT: {result}")
        raise HTTPException(status_code=502, detail="Bad response from GPT")

    for driver_result in json_result:
        for component_result in json_result[driver_result]:
            if int(driver_result) in results:
                if int(component_result) in results[int(driver_result)]:
                    results[int(driver_result)][int(component_result)] =\
                        json_result[driver_result][component_result]
    return results
