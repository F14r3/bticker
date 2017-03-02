from sqlalchemy import create_engine, Column, Integer, String, DateTime, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # engine = create_engine("mysql://scott:tiger@hostname/dbname",
    #                        encoding='latin1', echo=True)
    return create_engine(settings.DATABASE_URL, encoding='utf-8')


def create_deals_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Market(DeclarativeBase):
    """Sqlalchemy market model"""
    __tablename__ = "trading_market"

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String),


class Price(DeclarativeBase):
    """Sqlalchemy prices model"""
    __tablename__ = "trading_price"

    id = Column(Integer, primary_key=True)
    market_id = Column('market_id', Integer, nullable=False)
    ask = Column('ask', Numeric(16, 8), nullable=False)
    bid = Column('bid', Numeric(16, 8), nullable=False)
    volume = Column('volume', Numeric(16, 8), nullable=False)
    status = Column('status', Integer, nullable=True)
    created_at = Column('created_at', DateTime, nullable=False)
    UniqueConstraint('market_id', 'created_at', name='trading_price_market_id_45bff46b_uniq')
