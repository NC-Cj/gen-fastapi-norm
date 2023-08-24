from contextlib import contextmanager

from ...dao.db import my_session
from ...pkg.error import DatabaseFailure


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
                except Exception as e:
                    session.rollback()
                    raise DatabaseFailure(e) from e

    return wrapper
