from Tests.Fixtures.aception_fixture import aception


def test_incomplete_words_in_traintext_shouldnt_count_as_word(
        aception: aception):
    train_text = "mu en com"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 0


def test_incomplete_words_in_aception_shouldnt_count_as_word(
        aception: aception):
    train_text = "muys abuenas acomunicación"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 0
