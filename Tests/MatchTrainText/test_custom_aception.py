from Tests.MatchTrainText.Fixtures.aception_fixture import aception


def test_custom_traintext(aception: aception):
    train_text = "tienen los productos que pido, el pedido llega a tiempo buena atención del vendedor y repartidores"
    aception.MatchTrainText(train_text)
    assert not aception.didItMatch
