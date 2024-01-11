from openai import OpenAI
from dotenv import dotenv_values

config = dotenv_values("settings.env")

api_key = config["OPENAI_API_KEY"]

client = OpenAI(api_key=api_key)


def fix_grammar(traintext: str):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Corrige la ortografía, gramática y puntuación."
            },
            {
                "role": "user",
                "content": traintext
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
