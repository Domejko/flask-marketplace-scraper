from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database

from app.config import settings as set


# Defining the Base class
# The Base class is used as a base for all the models (tables) that will be created in the database.
Base = declarative_base()

# The SQL_DATABASE_URL is a string that contains the necessary information to connect to the PostgreSQL database. It
# includes the username, password, hostname, port, and database name.
SQL_DATABASE_URL = (f'postgresql://{set.database_username}:{set.database_password}@'
                    f'{set.database_hostname}:{set.database_port}/{set.database_name}')

# The engine is created using the create_engine() function from the SQLAlchemy library. It is used to connect to the
# database and perform operations on it.
engine = create_engine(SQL_DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)

# Checking if the database exists. If it doesn't exist, the create_database() function is called to create it.
if not database_exists(engine.url):
    create_database(engine.url)

# Creating session. It is responsible for creating sessions (database connections) to perform CRUD operations on the
# database. The sessions created with SessionLocal have autocommit and autoflush set to False, meaning that changes
# made in the session need to be explicitly committed or rolled back.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the tables.
Base.metadata.create_all(bind=engine)


