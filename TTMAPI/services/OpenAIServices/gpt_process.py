from openai import OpenAI
import json
from dotenv import dotenv_values

from TTMAPI.services.Playground import get_prompt

config = dotenv_values("settings.env")

api_key = config["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)


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
        session,
        answer_text: str,
        answer_type: str,
        commerce_type: str,
        model: str,
        drivers,
        logger):
    """
    Junta la instrucción con el contexto y la respuesta del usuario,
    y llama a GPT para obtener la respuesta del sistema.
    Retorna la respuesta del sistema y un error si lo hay.
    """
    logger.info(
        f"Experiencia: {answer_text}, Type: {answer_type}, Model: {model}")
    # Cambiar a True para probar sin llamar a GPT
    testing = False

    # Separar los componentes y UTs para contexto
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

    # Obtener la instrucción del prompt y unirla de forma correcta
    prompt = get_prompt(
        session=session,
        prompt_id=1,
        logger=logger)
    prompt_modifiable_instruction = prompt.modifiable_instruction
    prompt_unmodifiable_instruction = prompt.unmodifiable_instruction
    prompt_answer_example = prompt.answer_example
    prompt_instruction = "###Instrucción###\n" +\
        f"{prompt_modifiable_instruction}" +\
        f"\n{prompt_unmodifiable_instruction}" +\
        f"\n\n###Ejemplo de Respuesta###\n{prompt_answer_example}"

    # Unir la instrucción con el contexto
    system_instruction = f"{prompt_instruction}\n\n###Context###\n" +\
        f"Componentes:\n{components}\nUnidades Tácticas:\n{uts}"

    # Descomentar para ver el prompt de sistema
    logger.debug(f"system_instruction: {system_instruction}")

    # Definir prefijo de la experiencia del usuario según el tipo de respuesta
    if commerce_type is not None and commerce_type != "":
        user_experience = "Al ser cliente de un comercio " +\
            f"enfocado en {commerce_type}, "
    else:
        user_experience = ""
    if answer_type == "MB":
        user_experience += "mi buena experiencia se sustenta en: "
    elif answer_type == "B":
        user_experience += "mi experiencia podría mejorar en: "
    elif answer_type == "M":
        user_experience += "mi mala experiencia se sustenta en: "
    user_experience += answer_text

    # Descomentar para ver el prompt de usuario
    logger.debug(f"user_experience: {user_experience}")

    # Crear resultados vacíos para llenar con GPT
    results = create_empty_results(drivers)

    # Llamar a GPT
    if not testing:
        exception = None
        try:
            completion = client.chat.completions.create(
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
            result = completion.choices[0].message.content
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
