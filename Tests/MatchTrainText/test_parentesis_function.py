from Tests.MatchTrainText.Fixtures.aception_fixture import\
    (aception_with_parenthesis, aception_with_slash)


def test_traintext_with_base_of_aception_parenthesis_should_match(
        aception_with_parenthesis: aception_with_parenthesis):
    train_text = "$ Atiende $"
    aception_with_parenthesis.MatchTrainText(train_text)
    assert aception_with_parenthesis.didItMatch


def test_traintext_with_aception_with_parenthesis_should_match(
        aception_with_parenthesis: aception_with_parenthesis):
    train_text = "$ Atienden $"
    aception_with_parenthesis.MatchTrainText(train_text)
    assert aception_with_parenthesis.didItMatch


def test_traintext_with_one_of_slash_options_should_match(
        aception_with_slash: aception_with_slash):
    train_text = "Trato $"
    aception_with_slash.MatchTrainText(train_text)
    assert aception_with_slash.didItMatch


def test_traintext_with_another_slash_option_should_match(
        aception_with_slash: aception_with_slash):
    train_text = "$ Trataron"
    aception_with_slash.MatchTrainText(train_text)
    assert aception_with_slash.didItMatch


def test_traintext_with_only_base_of_slash_options_shouldnt_match(
        aception_with_slash: aception_with_slash):
    train_text = "$ Trat $"
    aception_with_slash.MatchTrainText(train_text)
    assert not aception_with_slash.didItMatch
