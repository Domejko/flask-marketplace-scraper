import pytest

import app.connect


@pytest.mark.parametrize('id, search_term, page_number, url', [
    (1, 'find test item', 3, 'http://www.test.com/s?k={search}&page={page}'),
    (2, 'test', 'test', 'http://www.test.com/s?k={search}&page={page}')
])
def test_get_url(id: int, search_term: str, page_number: int, url: str) -> None:
    if id == 1:
        assert app.connect.get_url(search_term, page_number, url) == 'http://www.test.com/s?k=find+test+item&page=3'
    else:
        with pytest.raises(ValueError, match=r'.*Incorrect .*'):
            app.connect.get_url(search_term, page_number, url)


@pytest.mark.parametrize('url', [
    'http://www.amazon.nl/s?k={search}&page={page}',
    'https://www.marktplaats.nl/q/{search}/p/{page}/#f:30|searchInTitleAndDescription:tru'
])
def test_connection(url: str) -> None:
    assert app.connect.connection(url)[1].status_code == 200


def test_connection_failure() -> None:
    assert app.connect.connection('https://www.20thcenturystudios.com/404')[1].status_code == 404
    # with pytest.raises(Exception, match=r".*Number of connection attempts exceeded.*"):
    #     app.connect.connection('https://www.20thcenturystudios.com/404')


def test_connection_incorrect_url() -> None:
    with pytest.raises(Exception, match=r".*The address you're trying to connect to is incorrect.*"):
        app.connect.connection('foo bar baz')
