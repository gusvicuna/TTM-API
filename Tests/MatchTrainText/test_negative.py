from Tests.MatchTrainText.Fixtures.aception_fixture import\
    aception_with_line
from Tests.Fixtures.aception_fixture import aception


def test_aception_with_line_negative_should_be_negative(
        aception_with_line: aception_with_line):
    train_text = "Atiende"
    aception_with_line.MatchTrainText(train_text)
    assert aception_with_line.isNegative


def test_aception_without_line_negative_shouldnt_be_negative(
        aception: aception):
    train_text = "Atiende"
    aception.MatchTrainText(train_text)
    assert not aception.isNegative
