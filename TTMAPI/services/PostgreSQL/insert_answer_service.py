from fastapi import HTTPException
from TTMAPI.models.sqlalchemy_models import Answer


def insert_answer(session, answer_data, survey, logger):
    try:
        answer = Answer(
            token=answer_data["token"],
            answer=answer_data["answer"],
            survey=survey)
        session.add(answer)
        session.flush()
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=e)
    return answer
