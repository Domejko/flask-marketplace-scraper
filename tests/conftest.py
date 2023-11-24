import os
import typing
from unittest import mock

import pytest
from bs4 import BeautifulSoup
from flask import Flask
from pytest import MonkeyPatch
from sqlalchemy.orm import Session
from sqlalchemy_utils import drop_database

import app.models.db_models
import tests.database
from app import view
from app.engine import SearchEngine
from tests.constants import (TEST_URL, TEST_BASE_URL, TEST_MAIN_TAGS, TEST_FIND_ALL_TAG,
                             TEST_PAGE_TAGS, test_html)


T = typing.TypeVar('T')


class Fixture(typing.Generic[T]):
    pass


@pytest.fixture
def search_engine() -> SearchEngine:
    return SearchEngine(url=TEST_URL,
                        base_url=TEST_BASE_URL,
                        main_tags=TEST_MAIN_TAGS,
                        find_all_tag=TEST_FIND_ALL_TAG,
                        page_tags=TEST_PAGE_TAGS,
                        db_model=app.models.db_models.Amazon,
                        db=tests.database)


@pytest.fixture
def response(monkeypatch: MonkeyPatch) -> (bytes, str):
    if os.path.isdir('./functional'):
        path = './functional/test_response.txt'
    else:
        path = 'tests/functional/test_response.txt'
    with open(path, 'rb') as f:
        response = f.read()

    return response, ''


@pytest.fixture
def soup() -> list[BeautifulSoup]:
    result = BeautifulSoup(test_html[0], 'html.parser')

    return [result]


@pytest.fixture
def drop_test_database():
    drop_database(tests.database.engine.url)


@pytest.fixture
def drop_test_tables():
    tests.database.Base.metadata.drop_all(bind=tests.database.engine)


@pytest.fixture
def session() -> Session:
    tests.database.Base.metadata.drop_all(bind=tests.database.engine)
    tests.database.Base.metadata.create_all(bind=tests.database.engine)
    db = tests.database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def my_app() -> Flask:
    test_app = Flask(__name__)
    test_app.config['TESTING'] = True

    test_app.register_blueprint(view)

    return test_app


@pytest.fixture
def client(my_app: Flask) -> Flask:
    with my_app.test_client() as client:
        yield client


@pytest.fixture()
def mock_marktplaats() -> mock.Mock:
    class MockMarktplaats:
        def main_search(self, query):
            return [{'Item': 'iPhone 11',
                     'Price': 699.99,
                     'Link': 'https://marktplaats.nl/iPhone',
                     'Img': 'https://marktplaats.nl/iPhone.jpg'}]

    yield MockMarktplaats()


@pytest.fixture()
def mock_ebay() -> mock.Mock:
    class MockEbay:
        def main_search(self, query):
            return [{'Item': 'iPhone 11 Pro',
                     'Price': 999.99,
                     'Link': 'https://eBay.nl/iPhone',
                     'Img': 'https://eBay.nl/iPhone.jpg'}]

    yield MockEbay()


@pytest.fixture()
def mock_amazon() -> mock.Mock:
    class MockAmazon:
        def main_search(self, query):
            return [{'Item': 'iPhone XR',
                     'Price': 599.99,
                     'Link': 'https://Amazon.nl/iPhone',
                     'Img': 'Amazon.nl/iPhone.jpg'}]

    yield MockAmazon()
