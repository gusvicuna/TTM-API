from Tests.MatchTrainText.Fixtures.aception_fixture import aception


def test_custom_traintext(aception: aception):
    train_text = "vendedor y repartidores"
    aception.MatchTrainText(train_text)
    assert not aception.didItMatch
