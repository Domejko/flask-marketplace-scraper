from pytest import MonkeyPatch
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
import pytest

from app.models.db_models import Amazon
from app.engine import SearchEngine
from tests.conftest import Fixture
from tests.constants import test_search_object, test_link, TEST_MAIN_TAGS


def test_url_search(search_engine: Fixture[SearchEngine]) -> None:
    result = search_engine.url_search(test_search_object)
    assert len(result) != 0


def test_main_page_search(search_engine: Fixture[SearchEngine], monkeypatch: MonkeyPatch,
                          soup: Fixture[list[BeautifulSoup]]) -> None:

    monkeypatch.setattr(SearchEngine, 'url_search', lambda x, y: soup)
    items_list = search_engine.main_page_scrape(test_search_object)
    assert items_list[0]['Price'] == 1750


def test_main_page_search_failure(search_engine: Fixture[SearchEngine], monkeypatch: MonkeyPatch) -> None:

    monkeypatch.setattr(SearchEngine, 'url_search', lambda x, y: [])
    items_list = search_engine.main_page_scrape(test_search_object)
    assert items_list is False


def test_get_links(search_engine: Fixture[SearchEngine], monkeypatch: MonkeyPatch,
                   soup: Fixture[list[BeautifulSoup]]) -> None:

    monkeypatch.setattr(SearchEngine, 'url_search', lambda x, y: soup)
    links_list = search_engine.get_links(test_search_object)
    assert links_list[0] == ('http://www.amazon.nl/Lenovo-Gaming-Laptop-Windows-Toetsenbord/dp/B0CG6P1P64/ref=sr_1_5'
                             '?keywords=Legion+5+Pro&qid=1697543635&sr=8-5')


def test_page_scrape(search_engine: Fixture[SearchEngine], monkeypatch: MonkeyPatch,
                     response: Fixture[bytes]) -> None:

    monkeypatch.setattr(SearchEngine, 'get_links', lambda x, y: test_link)
    monkeypatch.setattr('app.connect.connection', lambda x: response)
    items_list = search_engine.page_scrape(test_search_object)
    assert items_list[0]['Price'] == 1599


def test_page_scrape_failure(search_engine: Fixture[SearchEngine], monkeypatch: MonkeyPatch,
                             response: Fixture[bytes]) -> None:

    monkeypatch.setattr(SearchEngine, 'get_links', lambda x, y: [])
    monkeypatch.setattr('app.connect.connection', lambda x: response)
    items_list = search_engine.page_scrape(test_search_object)
    assert items_list is False


def test_save_to_database(search_engine: Fixture[SearchEngine], session: Fixture[Session]) -> None:

    items_list = [{'Item': 'test item', 'Price': 1599, 'Link': 'test item link'}]
    search_engine.save_to_database(items_list)
    db_response = session.query(Amazon).filter_by(item='test item').first()
    assert db_response.item == 'test item'
    assert db_response.price == '1599'
    assert db_response.link == 'test item link'


def test_find_tags(search_engine: Fixture[SearchEngine], soup: Fixture[list[BeautifulSoup]]) -> None:

    result_dict = search_engine.find_tags(soup[0], TEST_MAIN_TAGS)
    assert result_dict['Item'] == ('Lenovo Gaming Laptop Legion Pro 5 16ARX8 | 16" | AMD Ryzen 7 7745HX | 32GB RAM | 1 '
                                   'TB SSD | Windows OS | QWERTY Toetsenbord')
    assert result_dict['Img'] == 'https://m.media-amazon.com/images/I/715yUn1+QrL._AC_UL320_.jpg'
    assert result_dict['Price'] == 1750
    assert result_dict['Link'] == ('http://www.amazon.nl/Lenovo-Gaming-Laptop-Windows-Toetsenbord/dp/B0CG6P1P64/ref'
                                   '=sr_1_5?keywords=Legion+5+Pro&qid=1697543635&sr=8-5')


@pytest.mark.parametrize('id, tag', [
    (1, {'Img': ['img', 'id', 'landingImage', 'abc']}),
    (2, {'Item': ['span', 'class', 'a-size-large product-title-word-break', 22]}),
    (3, {'Price': ['span', 'class', 'a-price-whole']})
])
def test_find_tags_failure(search_engine: Fixture[SearchEngine], soup: Fixture[list[BeautifulSoup]],
                           id: int, tag: dict) -> None:

    if id in [1, 2]:
        with pytest.raises(Exception, match=r'.*Tag constant improperly formatted.*'):
            search_engine.find_tags(soup[0], tag)
    else:
        with pytest.raises(IndexError, match=r'.*list index out of range*'):
            search_engine.find_tags(soup[0], tag)


def test_page_search_with_results(monkeypatch: MonkeyPatch, search_engine: Fixture[SearchEngine]):
    expected_result = [{'Item': 'test item', 'Price': 1599, 'Link': 'test item link'}]
    monkeypatch.setattr(SearchEngine, 'page_scrape', lambda x, y: expected_result)
    search_result = search_engine.search(search_engine.page_scrape, 'example')
    assert search_result == expected_result


def test_page_search_without_results(monkeypatch: MonkeyPatch, search_engine: Fixture[SearchEngine]):
    expected_result = [{'Msg': 'No Results Found. http://www.amazon.nl/s?k={search}&page={page}'}]
    monkeypatch.setattr(SearchEngine, 'page_scrape', lambda x, y: False)
    search_result = search_engine.search(search_engine.page_scrape, 'example')
    assert search_result == expected_result


def test_main_search_with_results(monkeypatch: MonkeyPatch, search_engine: Fixture[SearchEngine]):
    expected_result = [{'Item': 'test item', 'Price': 1599, 'Link': 'test item link'}]
    monkeypatch.setattr(SearchEngine, 'main_page_scrape', lambda x, y: expected_result)
    search_result = search_engine.search(search_engine.main_page_scrape, 'example')
    assert search_result == expected_result


def test_main_search_without_results(monkeypatch: MonkeyPatch, search_engine: Fixture[SearchEngine]):
    expected_result = [{'Msg': 'No Results Found. http://www.amazon.nl/s?k={search}&page={page}'}]
    monkeypatch.setattr(SearchEngine, 'main_page_scrape', lambda x, y: False)
    search_result = search_engine.search(search_engine.main_page_scrape, 'example')
    assert search_result == expected_result
