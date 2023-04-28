from Tests.MatchTrainText.Fixtures.aception_fixture import aception


def test_custom_traintext(aception: aception):
    train_text = "trato"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 100
