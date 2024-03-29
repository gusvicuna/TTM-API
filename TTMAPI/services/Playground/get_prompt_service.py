from fastapi import HTTPException

from TTMAPI.models.sqlalchemy_models import Prompt


def get_prompt_service(session, prompt_id: str, logger):
    try:
        prompt = session.query(Prompt).filter_by(
            id=prompt_id).first()
    except Exception as e:
        session.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)

    if not prompt:
        logger.error(f"Prompt {prompt_id} not found")
        raise HTTPException(status_code=404, detail="Prompt not found")

    return prompt
