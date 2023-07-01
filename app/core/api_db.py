from functools import wraps
from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from ..dao.postgresql import get_session
from ..pkg.error import DatabaseFailure


def with_db_session(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with get_session() as session:
            return fn(*args, session=session, **kwargs)

    return wrapper


@with_db_session
def query_all(model, session: Session, **kwargs):
    return session.query(model).filter_by(**kwargs).all()


@with_db_session
def query_first(model, session: Session, **kwargs):
    return session.query(model).filter_by(**kwargs).first()


@with_db_session
def insert_many(model, session: Session, data: List[dict]):
    try:
        models = [model(**d) for d in data]
        session.bulk_save_objects(models)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@with_db_session
def insert_one(model, session: Session, data: dict):
    try:
        instance = model(**data)
        session.add(instance)
        session.flush()
        session.refresh(instance)
        return instance
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@with_db_session
def update_many(model, session: Session, data: dict, limit: Optional[int] = 100):
    try:
        session.query(model).filter_by(**data.pop('filter', {})).update(data, synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@with_db_session
def update_one(model, session: Session, data: dict, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        return None
    try:
        for key, value in data.items():
            setattr(instance, key, value)
        session.commit()
        return instance
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@with_db_session
def upsert(model, session: Session, data: dict, **kwargs):
    try:
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
            session.merge(instance)
        else:
            instance = model(**data)
            session.add(instance)
        session.commit()
        return instance
    except IntegrityError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@with_db_session
def delete_many(model, session: Session, **kwargs):
    try:
        session.query(model).filter_by(**kwargs).delete(synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@with_db_session
def delete_one(model, session: Session, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        return None
    try:
        session.delete(instance)
        session.commit()
        return instance
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e
