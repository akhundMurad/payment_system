from backend.database.config import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Common:
    def __init__(self, q: str, minimum: int = 0, maximum: int = 50):
        self.q = q
        self.minimum = minimum
        self.maximum = maximum
