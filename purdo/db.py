"""Database setup.

- Engine and session factory for the SQLite store; the path comes from
  DATABASE_URL so the backend can be swapped without touching the models.
- `Base`, the declarative base every model inherits from.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///purdo.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()

class Base(DeclarativeBase):
    pass

