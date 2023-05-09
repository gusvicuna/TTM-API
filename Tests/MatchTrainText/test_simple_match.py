from Tests.Fixtures.aception_fixture import aception


def test_same_text_should_match(
        aception: aception):
    train_text = "ab cde fghi"
    aception.MatchTrainText(train_text)
    assert aception.didItMatch


def test_traintext_has_aception_should_match(
        aception: aception):
    train_text = "- ab cde fghi -"
    aception.MatchTrainText(train_text)
    assert aception.didItMatch


def test_traintext_has_begining_of_aception_shouldnt_match(
        aception: aception):
    train_text = "- ab cde"
    aception.MatchTrainText(train_text)
    assert not aception.didItMatch


def test_traintext_has_ending_of_aception_shouldnt_match(
        aception: aception):
    train_text = "cde fghi -"
    aception.MatchTrainText(train_text)
    assert not aception.didItMatch
