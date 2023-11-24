import dotenv
from _pytest.monkeypatch import MonkeyPatch
from flask import Flask
from app import create_app


def test_create_app_development_config(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv('FLASK_ENV', 'development')

    app = create_app()

    assert isinstance(app, Flask)
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is False


def test_create_app_production_config(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv('FLASK_ENV', 'production')

    app = create_app()

    assert isinstance(app, Flask)
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is False


def test_create_app_testing_config(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv('FLASK_ENV', 'testing')

    app = create_app()

    assert isinstance(app, Flask)
    assert app.config['DEBUG'] is False
    assert app.config['TESTING'] is True


def test_create_app_default_config(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.delenv('FLASK_ENV', raising=False)

    app = create_app()

    assert isinstance(app, Flask)
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is False


def test_create_app_load_dotenv(monkeypatch: MonkeyPatch) -> None:
    def mock_load_dotenv(dotenv_path):
        assert dotenv_path == '.env.development'

    monkeypatch.setenv('FLASK_ENV', 'development')
    monkeypatch.setattr(dotenv, 'load_dotenv', mock_load_dotenv)

    app = create_app()

    assert isinstance(app, Flask)
