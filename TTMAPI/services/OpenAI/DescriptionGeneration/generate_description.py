import openai
from dotenv import dotenv_values

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]


def generate_description(name, phrases, logger):
    prompt_instruction_file = "TTMAPI/services/OpenAI/" +\
        "/DescriptionGeneration/description_generation_prompt.txt"
    prompt_example_file = "TTMAPI/services/OpenAI/" +\
        "/DescriptionGeneration/description_generation_example.txt"

    with open(prompt_instruction_file, 'r', encoding='utf-8') as file:
        prompt_instruction: str = file.read()
    with open(prompt_example_file, 'r', encoding='utf-8') as file:
        prompt_example: str = file.read()
    prompt_instruction += "\n" + prompt_example

    component = {}
    component["name"] = name
    component["phrases"] = phrases

    logger.info(f"Component: {component['name']}")

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
        return result
    except Exception as e:
        logger.error(f"Error: {e}, GPT: {result}")
        return name
