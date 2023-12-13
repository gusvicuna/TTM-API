from fastapi import APIRouter, Depends

from TTMAPI.config.db import getPostgreSQL
from TTMAPI.helpers.log import get_logger
from TTMAPI.models.prompt import Prompt
from TTMAPI.services.Playground import (
    get_prompt,
    update_prompt
)


router = APIRouter()
logger = get_logger(__name__)
base_route = "/prompt"


@router.get("/{prompt_id}")
async def get_prompt_instruction(
        prompt_id: int,
        session=Depends(getPostgreSQL)
        ):
    """
    Get prompt from database and return it
    """
    logger.info(f"GET {base_route}/{prompt_id}")
    prompt = get_prompt(
        session=session,
        prompt_id=prompt_id,
        logger=logger)
    return prompt


@router.put("/{prompt_id}")
async def update_prompt_instruction(
        prompt_id: int,
        prompt: Prompt,
        session=Depends(getPostgreSQL)):
    """
    Update prompt from database and return it
    """
    logger.info(f"PUT {base_route}/{prompt_id} prompt='{prompt}'")
    prompt = update_prompt(
        session=session,
        prompt_id=prompt_id,
        modifiable_instruction=prompt.modifiable_instruction,
        logger=logger)
    return prompt
