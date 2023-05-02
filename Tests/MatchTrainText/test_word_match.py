from Tests.Fixtures.aception_fixture import aception


def test_incomplete_words_in_traintext_shouldnt_count_as_word(
        aception: aception):
    train_text = "a de gh"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 0


def test_incomplete_words_in_aception_shouldnt_count_as_word(
        aception: aception):
    train_text = "abx ycde zfghiz"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 0


def test_repeated_words_should_not_add_to_the_count_of_matched_words(
        aception: aception):
    train_text = "ab ab ab"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() != 100
