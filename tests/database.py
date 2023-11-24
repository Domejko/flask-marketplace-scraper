from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from app.config import settings as set
from app.database import Base


SQLALCHEMY_DATABASE_URL = (f'postgresql://{set.database_username}:{set.database_password}@'
                           f'{set.database_hostname}:{set.database_port}/{set.test_database_name}')

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, echo=True)

if not database_exists(engine.url):
    create_database(engine.url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
