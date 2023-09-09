from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from app.utils.errors.error import DatabaseFailure
from ...dao.db import my_session


@contextmanager
def get_session():
    session = my_session()
    try:
        yield session
    finally:
        session.close()


def auto_session(fn):
    def wrapper(*args,
                **kwargs):
        if not kwargs.get("session"):
            with get_session() as session:
                try:
                    return fn(*args, session=session, **kwargs)
                except (SQLAlchemyError, Exception) as e:
                    session.rollback()
                    raise DatabaseFailure(e) from e

    return wrapper
