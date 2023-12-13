from TTMAPI.models.sqlalchemy_models import Prompt
from fastapi import HTTPException


def update_prompt_service(
        session,
        modifiable_instruction: str,
        prompt_id: str,
        logger):
    """
    Update a prompt in the database
    """
    try:
        prompt = session.query(Prompt).filter_by(
            id=prompt_id).update(
                {
                    "modifiable_instruction": modifiable_instruction,
                }
            )
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)

    if not prompt:
        logger.error(f"Prompt {prompt_id} not found")
        raise HTTPException(status_code=404, detail="Prompt not found")

    return prompt
