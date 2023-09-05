from TTMAPI.models.sqlalchemy_models import Aception


def insert_aception(session, phrase, component):
    aception = Aception(
        phrase=phrase,
        component=component)
    session.add(aception)
    session.flush()
    return aception
