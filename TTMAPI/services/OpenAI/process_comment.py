import openai
import json
from dotenv import dotenv_values

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def gpt_process(traintext: str, logger):

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
    logger.info(f"gptresponse: {response['choices'][0]['message']['content']} :end")
    json_result = json.loads(response["choices"][0]["message"]["content"])
    return json_result
