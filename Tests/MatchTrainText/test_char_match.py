from Tests.Fixtures.aception_fixture import aception


def test_same_text_has_100_percent_charmatch(
        aception: aception):
    train_text = "ab cde fghi"
    aception.MatchTrainText(train_text)
    assert aception.getCharPercent() == 100


def test_traintext_has_aception_must_have_100_percent_charmatch(
        aception: aception):
    train_text = "ab cde fghi. jkl mno pqr"
    aception.MatchTrainText(train_text)
    assert aception.getCharPercent() == 100
