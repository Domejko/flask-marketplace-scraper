from _pytest.fixtures import FixtureFunction
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import inspect

from tests.conftest import Fixture
from tests.database import engine
from app.models.db_models import Amazon


def test_database_exists(session: Fixture[Session]) -> None:
    assert database_exists(engine.url) is True


def test_create_database(session: Fixture[Session], drop_test_database: Fixture) -> None:
    database_url = engine.url
    create_database(database_url)
    assert database_exists(database_url) is True


def test_session_creation(session: Fixture[Session]) -> None:
    assert session is not None


def test_table_creation(session: Fixture[Session], drop_test_tables: Fixture) -> None:
    Amazon.metadata.create_all(bind=engine)
    assert inspect(engine).has_table('amazon') is True
