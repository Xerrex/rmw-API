from .db_setup import SessionLocal


def get_db():
    """Get DB dependency
    """
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()