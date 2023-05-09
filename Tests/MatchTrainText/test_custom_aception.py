from Tests.MatchTrainText.Fixtures.aception_fixture import aception


def test_custom_traintext(aception: aception):
    train_text = "Muy buen trato. rapido y sencillo"
    aception.MatchTrainText(train_text)
    assert aception.getCharPercent() < 100
