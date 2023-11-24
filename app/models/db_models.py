from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

import app.database


class Amazon(app.database.Base):
    """
    Description:
        This class represents a table called 'amazon' in the database.
    """
    __tablename__ = 'amazon'
    id = Column(Integer, nullable=False, primary_key=True)
    item = Column(String, nullable=False)
    price = Column(String, nullable=False)
    link = Column(String, nullable=False, unique=True)
    rating = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class EBay(app.database.Base):
    """
    Description:
        This class represents a table called 'ebay' in the database.
    """
    __tablename__ = 'ebay'
    id = Column(Integer, nullable=False, primary_key=True)
    item = Column(String, nullable=False)
    price = Column(String, nullable=False)
    link = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Marktplaats(app.database.Base):
    """
    Description:
        This class represents a table called 'marktplaats' in the database.
    """
    __tablename__ = 'marktplaats'
    id = Column(Integer, nullable=False, primary_key=True)
    item = Column(String, nullable=False)
    price = Column(String, nullable=False)
    link = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


app.database.Base.metadata.create_all(bind=app.database.engine)
