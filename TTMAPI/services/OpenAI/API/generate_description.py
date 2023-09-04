import openai
from dotenv import dotenv_values
from fastapi import HTTPException

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def generate_description(name, phrases, logger):
    prompt_instruction_file = "TTMAPI/services/OpenAI/" +\
        "description_generation_prompt.txt"
    with open(prompt_instruction_file, 'r') as file:
        prompt_instruction: str = file.read()

    component = {}
    component["name"] = name
    component["phrases"] = phrases
    
    print(component)

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

        logger.info(f"gptresponse: {result}")
    except Exception as e:
        logger.error(f"{e}, GPT: {result}")
        raise HTTPException(status_code=502, detail="Bad response from GPT")
    return result
