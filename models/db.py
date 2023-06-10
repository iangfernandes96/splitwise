#!/usr/bin/python3

# import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1/splitwise"
# os.environ['SQLALCHEMY_DATABASE_URL'] or
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:  # type: ignore
    try:
        db = SessionLocal()
        yield db
    except Exception:
        raise
    db.close()
