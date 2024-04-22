from sqlalchemy.orm import Session
from app.db_config.database import SessionLocal
from app.core.settings import hms_settings


class ORMSessionMixin:
    """Base orm session mixin for interacting with the database."""

    def __init__(self):
        self.orm: Session = (
            self.get_db().__next__()
            # if not hms_settings.USE_TEST_DB
            # else _get_test_db().__next__()
        )

    def get_db(self):

        db = SessionLocal()
        try:
            yield db
        except Exception:
            db.rollback()
        finally:
            db.close()
