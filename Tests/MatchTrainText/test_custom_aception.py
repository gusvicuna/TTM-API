from Tests.MatchTrainText.Fixtures.aception_fixture import aception


def test_custom_traintext(aception: aception):
    train_text = "amable"
    aception.MatchTrainText(train_text)
    assert aception.didItMatch
