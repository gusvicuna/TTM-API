from pytest import fixture
from TTMAPI.models.aception import Aception


@fixture
def aception():
    return Aception(text="Muy buena comunicación")
