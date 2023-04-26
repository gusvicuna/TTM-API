from pytest import fixture
from TTMAPI.models.aception import Aception


@fixture
def aception():
    return Aception(text="Precios")


@fixture
def aception_with_at_symbol():
    return Aception(text="Amen@")
