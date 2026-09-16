from typing import Generator
from .db_setup import SessionLocal


def get_db()-> Generator:
    """Get DB dependency
    """
    try:
        db = SessionLocal()
        yield db
    finally: 
        db.close()
