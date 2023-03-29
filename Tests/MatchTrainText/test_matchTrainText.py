from Tests.Fixtures.aception_fixture import aception


def test_same_text_has_100_percent_charmatch(aception):
    train_text = "Muy buena comunicación"
    aception.MatchTrainText(train_text)
    assert aception.getCharPercent() == 100


def test_same_text_in_lower_case_has_100_percent_charmatch(aception):
    train_text = "muy buena comunicación"
    aception.MatchTrainText(train_text)
    assert aception.getCharPercent() == 100


def test_traintext_has_aception_must_have_100_percent_charmatch(aception):
    train_text = "Muy buena comunicación. Aunque pasó esto."
    aception.MatchTrainText(train_text)
    assert aception.getCharPercent() == 100


def test_aception_has_2_of_3_words_must_have_66_percent_charmatch(aception):
    train_text = "está muy buena."
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 66.67


def test_incomplete_words_shouldnt_count_as_word(aception):
    train_text = "mu"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 0
