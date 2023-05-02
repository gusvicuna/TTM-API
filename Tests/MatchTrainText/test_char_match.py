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


def test_aception_has_2_of_3_words_must_have_66_percent_charmatch(
        aception: aception):
    train_text = "ab cde jkl"
    aception.MatchTrainText(train_text)
    assert aception.getWordPercent() == 66.67
