from TTMAPI.config.db import getMongo
from fastapi import HTTPException


def get_prompt_service(prompt_id: str, logger):
    db = getMongo()
    try:
        prompt_cursor = db["prompts"].find_one({"id": prompt_id})
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)

    if not prompt_cursor:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return prompt_cursor
