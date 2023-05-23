from Tests.Fixtures.aception_fixture import aception


def test_correct_starting_position_of_match(aception: aception):
    train_text = "& ab cde fghi &"
    aception.MatchTrainText(train_text)
    assert aception.startingPosMatch == 2


def test_correct_ending_position_of_match(aception: aception):
    train_text = "& ab cde fghi &"
    aception.MatchTrainText(train_text)
    assert aception.endingPosMatch == 13
