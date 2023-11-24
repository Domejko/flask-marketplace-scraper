from app.config import Settings, get_config, ProductionConfig, DevelopmentConfig, TestingConfig


def test_settings() -> None:
    settings = Settings(database_hostname='test',
                        database_port='5555',
                        database_password='password',
                        database_name='test name',
                        test_database_name='test db',
                        database_username='test user')

    assert settings.database_hostname == 'test'
    assert settings.database_port == '5555'
    assert settings.database_password == 'password'
    assert settings.database_name == 'test name'
    assert settings.test_database_name == 'test db'
    assert settings.database_username == 'test user'


def test_get_config_prod() -> None:
    assert get_config('production') == ProductionConfig


def test_get_config_dev() -> None:
    assert get_config('development') == DevelopmentConfig


def test_get_config_test() -> None:
    assert get_config('testing') == TestingConfig

