from Tests.MatchTrainText.Fixtures.aception_fixture import aception


def test_custom_traintext(aception: aception):
    train_text = "de mi de"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() != 100
