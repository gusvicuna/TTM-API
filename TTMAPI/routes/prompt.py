from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger


router = APIRouter()
logger = get_logger(__name__)
base_route = "/prompt"


@router.get("/{prompt_id}")
async def get_prompt_instruction(prompt_id: int):
    """
    Get text from gpt_process_prompt.txt or description_generation.txt
    and return it as a string
    """
    logger.info(f"GET {base_route}/{prompt_id}")

    file_path = "TTMAPI/services/OpenAI/"

    if (prompt_id == 1):
        file_path += "GPTProcess/gpt_process_prompt.txt"
    elif (prompt_id == 2):
        file_path += "DescriptionGeneration/description_generation_prompt.txt"

    with open(file_path, "r", encoding='utf-8') as f:
        prompt = f.read()

    logger.debug(f"Prompt: {prompt}")

    return prompt


@router.put("/{prompt_id}")
async def modify_prompt_instruction(prompt_id: int, prompt_text: str):
    """
    Modify text from gpt_process_prompt.txt or description_generation.txt
    """
    logger.info(f"PUT {base_route}/{prompt_id} with body: {prompt_text}")

    file_path = "TTMAPI/services/OpenAI/"

    if (prompt_id == 1):
        file_path += "GPTProcess/gpt_process_prompt.txt"
    elif (prompt_id == 2):
        file_path += "DescriptionGeneration/description_generation_prompt.txt"

    with open(file_path, "w", encoding='utf-8') as f:
        f.write(prompt_text)

    return prompt_text
