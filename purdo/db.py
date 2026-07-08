"""Database setup: engine, session factory, and the declarative Base.

YOU WRITE THIS (Lesson 1). Spec:
- A SQLAlchemy engine pointing at sqlite:///purdo.db (path configurable via
  the DATABASE_URL env var, python-dotenv loaded).
- A session factory (sessionmaker) and a `get_session()` helper.
- The DeclarativeBase subclass `Base` that all models inherit from.
"""
