from TTMAPI.models.sqlalchemy_models import Answer


def insert_answer(session, answer_data, survey):
    answer = Answer(
        token=answer_data["token"],
        answer=answer_data["answer"],
        survey=survey)
    session.add(answer)
    session.flush()
