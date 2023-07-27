import openai
import json
from dotenv import dotenv_values

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def gpt_process(traintext: str, logger):

    full_result = {
        "REQUERIMIENTO": 0,
        "TIEMPOS": 0,
        "ECONOMICOS": 0,
        "APRENDIZAJE": 0,
        "RAPIDEZ": 0,
        "CONOCIMIENTO": 0,
        "ORIENTACION": 0,
        "EFECTIVIDAD COMUNICACIONAL": 0,
        "PRESENCIA": 0,
        "PROACTIVIDAD": 0,
        "TRATO": 0,
        "ACCIONES DE AMOR": 0,
        "PRECIOS": 0,
        "TASAS": 0,
        "CONDICIONES": 0,
        "CREDITO": 0,
        "CONFIANZA": 0,
        "HONESTIDAD": 0,
        "RESPETO": 0,
        "ECOLOGIA": 0,
        "FACILIDAD": 0,
        "FLUIDEZ": 0,
        "PRACTICIDAD": 0,
        "CALIDAD": 0,
        "VARIEDAD": 0,
        "DISENADOS PARA MI": 0,
        "DISPONIBILIDAD": 0,
        "TECNOLOGIA": 0,
        "FACILES DE VENDER": 0,
        "ENVOLTURA": 0,
        "SABOR": 0,
        "BAÑOS": 0,
        "ESTACIONAMIENTOS": 0,
        "MAQUINAS": 0,
        "SUCURSALES": 0,
        "LAYOUT": 0,
        "SECTORES DE ATENCION": 0,
        "APP": 0,
        "WEB ": 0,
        "MARCA": 0,
        "COLABORADOR": 0,
        "RELACIÓN COMERCIAL": 0,
        "PRODUCTO_SERVICIO": 0,
        "COMUNICACION_MKT": 0,
        "DISTRIBUCIÓN": 0,
        "INFRASTUCTURA_VIRTUAL": 0,
        "INFRASTUCTURA_FISICA": 0,
        "CONTACT_CENTER": 0,
    }

    with open("TTMAPI\services\OpenAI\prompt_instruction_simple.txt", 'r') as file:
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
    logger.info(f"gptresponse: {response['choices'][0]['message']['content']}")

    try:
        json_result = json.loads(response["choices"][0]["message"]["content"])
    except Exception as e:
        logger.error(e)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt_instruction},
                {"role": "user", "content": traintext},
                {"role": "assistant", "content": response['choices'][0]['message']['content']},
                {"role": "user", "content": e}],
            temperature=0.2,
            max_tokens=814,
            top_p=0.4,
            frequency_penalty=0,
            presence_penalty=0
        )
        json_result = json.loads(response["choices"][0]["message"]["content"])
    for key in json_result:
        if key in full_result:
            full_result[key] = json_result[key]
    return full_result
