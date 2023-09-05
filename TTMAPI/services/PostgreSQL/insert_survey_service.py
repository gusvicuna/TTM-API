from TTMAPI.models.sqlalchemy_models import Survey


def insert_survey(session, survey_data):
    survey = Survey(description=survey_data["description"])
    session.add(survey)
    session.flush()
    return survey
