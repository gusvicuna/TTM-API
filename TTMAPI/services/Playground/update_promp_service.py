from TTMAPI.config.db import getMongo
from TTMAPI.models.prompt import Prompt
from fastapi import HTTPException


def update_prompt_service(prompt: Prompt, prompt_id: str, logger):
    db = getMongo()
    try:
        prompt_cursor = db["prompts"].find_one({"id": prompt_id})
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    if prompt_cursor is not None:
        prompt.unmodifiable_instruction =\
            prompt_cursor["unmodifiable_instruction"]
        try:
            db["prompts"].replace_one(
                {"id": prompt_id},
                prompt.dict())
            return db["prompts"].find_one({"id": prompt_id})
        except Exception as e:
            logger.error(f"Error: {e}")
            raise HTTPException(status_code=500, detail=e)
    else:
        logger.error("Prompt not Found")
        raise HTTPException(status_code=404, detail="Prompt not found")
