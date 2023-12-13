from fastapi import APIRouter

from TTMAPI.helpers.log import get_logger
from TTMAPI.models.prompt import Prompt
from TTMAPI.services.Playground import (
    get_prompt_service,
    update_prompt_service
)


router = APIRouter()
logger = get_logger(__name__)
base_route = "/prompt"


@router.get("/{prompt_id}")
async def get_prompt_instruction(prompt_id: int):
    """
    Get prompt from get_prompt_service.py and return it
    """
    logger.info(f"GET {base_route}/{prompt_id}")
    prompt_cursor = get_prompt_service(prompt_id=prompt_id, logger=logger)
    prompt = Prompt(**prompt_cursor)
    return prompt


@router.put("/{prompt_id}")
async def update_prompt_instruction(prompt_id: int, prompt: Prompt):
    """
    Update prompt from update_prompt_service.py and return it
    """
    logger.info(f"PUT {base_route}/{prompt_id} prompt='{prompt}'")
    prompt_cursor = update_prompt_service(
        prompt_id=prompt_id,
        prompt=prompt,
        logger=logger)
    prompt = Prompt(**prompt_cursor)
    return prompt
