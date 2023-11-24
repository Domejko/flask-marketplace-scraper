from unittest.mock import Mock
from pytest import MonkeyPatch

from app.main import run_search
from app.engine import SearchEngine
from tests.conftest import Fixture


def test_run_search_main(search_engine: Fixture[SearchEngine], monkeypatch: MonkeyPatch,
                         response: Fixture[bytes]) -> None:

    monkeypatch.setattr('app.connect.connection', lambda x: response)
    monkeypatch.setattr('app.marktplaats_scrape.marktplaats', lambda x: search_engine)
    monkeypatch.setattr('app.ebay_scrape.ebay', lambda x: search_engine)
    monkeypatch.setattr('app.amazon_scrape.amazon', lambda x: search_engine)
    search_result = run_search('Legion 5 Pro', 0)
    assert search_result[0]['Item'] == ('LENOVO Legion Pro 5 16ARX8 (82WM00BEMH) | 16" | AMD Ryzen 7 7745HX | NVIDIA '
                                        'GeForce RTX 4060 | 32GB RAM | 1 TB SSD | Windows OS | QWERTY Toetsenbord')
    assert search_result[0]['Price'] == 1599
    assert search_result[0]['Link'] == 'http://www.amazon.nl/LENOVO-82WM00BEMH-GeForce-Windows-Toetsenbord/dp/B0CG6P1P64'
    assert search_result[0]['Img'] == 'https://m.media-amazon.com/images/I/715yUn1+QrL._AC_UL320_.jpg'


def test_run_search_page(search_engine: Fixture[SearchEngine], monkeypatch: MonkeyPatch,
                         response: Fixture[bytes]) -> None:

    monkeypatch.setattr('app.connect.connection', lambda x: response)
    monkeypatch.setattr('app.marktplaats_scrape.marktplaats', lambda x: search_engine)
    monkeypatch.setattr('app.ebay_scrape.ebay', lambda x: search_engine)
    monkeypatch.setattr('app.amazon_scrape.amazon', lambda x: search_engine)
    search_result = run_search('Legion 5 Pro', 3)
    assert search_result[-1]['Item'] == 'LENOVO Legion Pro 5 16ARX8 (82WM00BEMH)'
    assert search_result[-1]['Price'] == 1599
    assert search_result[-1]['Link'] == 'http://www.amazon.nl/LENOVO-82WM00BEMH-GeForce-Windows-Toetsenbord/dp/B0CG6P1P64'
    assert search_result[-1]['Img'] == 'https://m.media-amazon.com/images/I/715yUn1+QrL._AC_SY300_SX300_.jpg'
    assert search_result[-1]['Rating'] == ''


def test_run_search(mock_marktplaats: Fixture[Mock], mock_ebay: Fixture[Mock],
                    mock_amazon: Fixture[Mock], monkeypatch: MonkeyPatch) -> None:

    query = "iPhone"
    item_condition = 1

    monkeypatch.setattr('app.marktplaats_scrape.marktplaats', lambda x: mock_marktplaats)
    monkeypatch.setattr('app.ebay_scrape.ebay', lambda x: mock_ebay)
    monkeypatch.setattr('app.amazon_scrape.amazon', lambda x: mock_amazon)

    results = run_search(query, item_condition)

    assert len(results) == 3
    assert results[0]['Item'] == 'iPhone 11 Pro'
    assert results[0]['Price'] == 999.99
    assert results[0]['Link'] == 'https://eBay.nl/iPhone'
    assert results[0]['Img'] == 'https://eBay.nl/iPhone.jpg'
    assert results[1]['Item'] == 'iPhone 11'
    assert results[1]['Price'] == 699.99
    assert results[1]['Link'] == 'https://marktplaats.nl/iPhone'
    assert results[1]['Img'] == 'https://marktplaats.nl/iPhone.jpg'
    assert results[2]['Item'] == 'iPhone XR'
    assert results[2]['Price'] == 599.99
    assert results[2]['Link'] == 'https://Amazon.nl/iPhone'
    assert results[2]['Img'] == 'Amazon.nl/iPhone.jpg'
