from Tests.MatchTrainText.Fixtures.aception_fixture import aception_with_at_symbol


def test_traintext_with_same_aception_and_char_o_should_match_100_percent(aception_with_at_symbol):
    train_text = "Ameno"
    aception_with_at_symbol.MatchTrainText(train_text)
    assert aception_with_at_symbol.getWordPercent() == 100


def test_traintext_with_same_aception_and_char_a_should_match_100_percent(aception_with_at_symbol):
    train_text = "Amena"
    aception_with_at_symbol.MatchTrainText(train_text)
    assert aception_with_at_symbol.getWordPercent() == 100
