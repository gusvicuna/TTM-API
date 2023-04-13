from Tests.Fixtures.aception_fixture import aception


def test_not_concatenated_with_concatenated_option_false(
        aception: aception):
    train_text = "buena Muy comunicación"
    aception.MatchTrainText(train_text, concatenated=False)
    assert aception.getWordPercent() == 100


def test_not_concatenated_with_concatenated_option_true(
        aception: aception):
    train_text = "buena Muy comunicación"
    aception.MatchTrainText(train_text, concatenated=True)
    assert aception.getWordPercent() != 100


def test_concatenated_option_false_shouldnt_count_the_same_word_twice(
        aception: aception):
    train_text = "Muy muy buena comunicación"
    aception.MatchTrainText(train_text, concatenated=False)
    assert aception.mostWordsMatched == 3
