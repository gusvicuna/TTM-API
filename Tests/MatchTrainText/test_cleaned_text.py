from Tests.Fixtures.aception_fixture import aception


def test_different_cases_should_be_ignored(
        aception: aception):
    train_text = "AB cde FgHi"
    aception.MatchTrainText(train_text)
    assert aception.didItMatch


def test_acents_should_be_ignored(
        aception: aception):
    train_text = "áb cdé fghí"
    aception.MatchTrainText(train_text)
    assert aception.didItMatch
