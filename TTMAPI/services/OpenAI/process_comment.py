import openai
from dotenv import dotenv_values

from TTMAPI.models.driver import Driver

config = dotenv_values("settings.env")

openai.api_key = config["OPENAI_API_KEY"]

prompt_intro: str = "Given a customer feedback text and a predefined dictionary of" +\
        "'drivers' with their 'components' and 'meanings' found in the text, evaluate the sentiment of each 'meaning' based on its context." +\
        "Assign a sentiment value to each 'meaning': 0 if it does not appear in the text, 1 if it appears positively, -1 if it appears negatively, 2 if it is ambiguous or appears in both positive and negative context." +\
        "Return a dictionary with 'drivers' as keys, each containing a dictionary of 'components' with their own dictionaries." +\
        "Each 'component' dictionary will have 'meanings' as keys and their respective sentiment values as output.\n" +\
        "Im going to give you the input in the form:\nFeedback text:<text>\nDrivers:{<driver1>:{<component1>:[<meaning1>]}, <driver2>:{<component2>:[<meaning2>,<meaning3>]}}" +\
        "\nThe output should be in the form:{<driver1>:{<component1>:{<meaning1>:<sentiment>}}}"


def davinci_match(traintext: str, drivers: list[Driver]):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt_intro +
        f"Input:\nFeedback text:{traintext}\nDrivers:{drivers}",
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # output: str = response["choices"][0]["text"]
    # output = json.loads(output.replace("Output:", ""))
    return response


# result = get_polars(traintext="Su experiencia fue buena, el único problema que ha tenido es el stock del producto el cual afecta sus ventas",
#                     drivers='{"cumplimiento":{"Requerimiento":["Problema"]}, "productos/servicios":{"disponibilidad":["stock","producto"]},"Espiritu de atención":{"Trato": ["experiencia"]}}')
# print(result)
