from Tests.Fixtures.aception_fixture import aception


def test_different_cases_should_be_ignored(
        aception: aception):
    train_text = "mUy bUena comuNicacIóN"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 100


def test_acents_should_be_ignored(
        aception: aception):
    train_text = "Muy buena comunicacion"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 100
