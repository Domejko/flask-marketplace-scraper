from app.models.db_models import Amazon, Marktplaats, EBay


def test_amazon() -> None:
    amazon = Amazon(item='test item', price=1599, link='test link', rating=5)
    assert amazon.item == 'test item'
    assert amazon.price == 1599
    assert amazon.link == 'test link'
    assert amazon.rating == 5


def test_marktplaats() -> None:
    amazon = Marktplaats(item='test item', price=1599, link='test link')
    assert amazon.item == 'test item'
    assert amazon.price == 1599
    assert amazon.link == 'test link'


def test_ebay() -> None:
    amazon = EBay(item='test item', price=1599, link='test link')
    assert amazon.item == 'test item'
    assert amazon.price == 1599
    assert amazon.link == 'test link'
