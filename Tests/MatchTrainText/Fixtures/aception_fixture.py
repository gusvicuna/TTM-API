from pytest import fixture
from TTMAPI.models.aception import Aception


@fixture
def aception():
    return Aception(text="Amab(ilidad/le/les)")


@fixture
def aception_with_at_symbol():
    return Aception(text="Amen@")


@fixture
def aception_with_parenthesis():
    return Aception(text="Atiende(n)")


@fixture
def aception_with_slash():
    return Aception(text="Trat(o/os/en/an/aron)")
