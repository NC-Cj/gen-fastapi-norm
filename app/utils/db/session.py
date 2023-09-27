from contextlib import contextmanager

from sqlalchemy.exc import SQLAlchemyError

from ..errors.error import DatabaseException
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
                    raise DatabaseException(e) from e

    return wrapper
