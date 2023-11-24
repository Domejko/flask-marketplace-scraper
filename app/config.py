from typing import Type
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    """
    Documentation:
        The Settings class is a subclass of the BaseSettings class. It is used to define and manage various settings
        related to database configuration.

    Properties:
        database_hostname: A string representing the hostname of the database server.
        database_port: A string representing the port number on which the database server is listening.
        database_password: A string representing the password for accessing the database.
        database_name: A string representing the name of the main database.
        test_database_name: A string representing the name of the test database.
        database_username: A string representing the username for accessing the database.

    Attributes:
        model_config: An instance of the SettingsConfigDict class that provides configuration settings for the Settings
                    class. It is initialized with the env_file parameter pointing to the ../.env file.
    """
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    test_database_name: str
    database_username: str

    model_config = SettingsConfigDict(env_file='../.env')


settings = Settings()


class Config(object):
    """
    Description:
        Flask configuration class.
    """
    DEBUG = False
    TESTING = False
    TEMPLATES_AUTO_RELOAD = True

    # SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    """
    Description:
        Flask configuration class.
    """
    pass


class DevelopmentConfig(Config):
    """
    Description:
        Flask configuration class.
    """
    ENV = 'development'
    DEBUG = True

    # SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    """
    Description:
        Flask configuration class.
    """
    TESTING = True
    # SESSION_COOKIE_SECURE = False


def get_config(config: str) -> Type[Config]:
    """
    Description:
        Function that takes string as value and returns configuration class for Flask application.

    Parameters:
        config (str): "development", "production", "testing"

    Returns:
        configuration class """

    config_map = {'production': ProductionConfig,
                  'development': DevelopmentConfig,
                  'testing': TestingConfig}

    return config_map.get(config)
