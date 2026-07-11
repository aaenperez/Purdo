"""Database setup: engine, session factory, and the declarative Base.

YOU WRITE THIS (Lesson 1). Spec:
- A SQLAlchemy engine pointing at sqlite:///purdo.db (path configurable via
  the DATABASE_URL env var, python-dotenv loaded).
- A session factory (sessionmaker) and a `get_session()` helper.
- The DeclarativeBase subclass `Base` that all models inherit from.
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

