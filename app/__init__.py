import os

from dotenv import load_dotenv
from flask import Flask
from typing import Type

from app.config import ProductionConfig, DevelopmentConfig, TestingConfig, get_config, Config
from app.blueprints import view


def create_app() -> Flask:
    """
    Description:
        This function is responsible for creating Flask object with a configuration set accordingly to the
        give variable in FLASK_ENV and calls the Blueprints class instance. If FLASK_ENV is empty default configuration
        is set to development.

    Returns:
        The Flask application object that has been configured based on the specified environment.
    """

    load_dotenv('.env.development')
    flask_env = os.environ.get('FLASK_ENV') or 'development'

    app = Flask(__name__)
    conf: Type[Config] = get_config(flask_env)

    app.config.from_object(conf)
    app.register_blueprint(view)

    return app
