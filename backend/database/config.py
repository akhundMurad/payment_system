import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DB_URL = os.environ['SQLALCHEMY_DB_URL']

engine = create_engine(
    SQLALCHEMY_DB_URL
)

SessionLocal = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()
