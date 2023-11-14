import openai
import json
from dotenv import dotenv_values
from TTMAPI.models.prompt import Prompt

from TTMAPI.services.MongoDB import get_prompt_service

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def create_empty_results(drivers):
    results = {}
    for driver in drivers:
        results[driver.id] = {}
        for component in driver.components:
            results[driver.id][component.id] = 0
    return results


def verify_correct_result(json_data):
    # Asegurarse de que json_data es un diccionario
    if not isinstance(json_data, dict):
        return False

    for key, value in json_data.items():
        # Verificar si cada valor es un diccionario
        if not isinstance(value, dict):
            return False

        for sub_key, sub_value in value.items():
            if sub_value not in [0, 1, -1, 2]:
                return False

    return True


def gpt_process(
        answer_text: str,
        answer_type: str,
        model: str,
        drivers,
        logger):
    logger.info(
        f"Experiencia: {answer_text}, type:{answer_type} , Model: {model}")
    # Cambiar a True para probar sin llamar a GPT
    testing = False

    components = {}
    uts = {}
    for driver in drivers:
        if driver.driver_type == "drivers":
            components[driver.id] = {}
            for component in driver.components:
                components[driver.id][component.id] = component.description
        elif driver.driver_type == "ut":
            uts[driver.id] = {}
            for component in driver.components:
                uts[driver.id][component.id] = component.description
    # logger.debug(f"Components: {components}\nUTs: {uts}")

    prompt_cursor = get_prompt_service(prompt_id=1, logger=logger)
    prompt = Prompt(**prompt_cursor)
    prompt_modifiable_instruction = prompt.modifiable_instruction
    prompt_unmodifiable_instruction = prompt.unmodifiable_instruction

    prompt_instruction = prompt_modifiable_instruction + "\n" +\
        prompt_unmodifiable_instruction

    system_instruction = prompt_instruction +\
        f"\nComponentes:\n{components}\nUnidades Tácticas:\n{uts}"

    user_experience = ""
    if answer_type == "MB":
        user_experience = "Mi buena experiencia se sustenta: "
    elif answer_type == "B":
        user_experience = "Mi experiencia podría mejorar: "
    elif answer_type == "M":
        user_experience = "Mi mala experiencia se sustenta: "
    user_experience += answer_text

    results = create_empty_results(drivers)

    if not testing:
        exception = None
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_experience}],
                temperature=0.2,
                max_tokens=150,
                top_p=0.4,
                frequency_penalty=0,
                presence_penalty=0,
                stop=["Component"]
            )
            result = response['choices'][0]['message']['content']
            logger.info(f"gptresponse: {result}")
        except Exception as e:
            logger.error(f"Error: {e}")
            exception = e
            return results, exception

        try:
            corrected_result = result.replace("'", "\"")
            json_result = json.loads(corrected_result)
        except Exception as e:
            logger.error(f"General Error: {e}, GPT: {result}")
            exception = e
            return result, exception

        if not verify_correct_result(json_result):
            logger.error(f"Formato erroneo, GPT: {result}")
            return result, f"Formato erroneo, GPT: {result}"

        for driver_result in json_result:
            for component_result in json_result[driver_result]:
                if int(driver_result) in results:
                    if int(component_result) in results[int(driver_result)]:
                        results[int(driver_result)][int(component_result)] =\
                            json_result[driver_result][component_result]
    return results, None
