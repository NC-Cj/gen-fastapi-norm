from functools import wraps
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from ..dao.postgresql import get_session
from ..pkg.error import DatabaseFailure


def __depends(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with get_session() as session:
            return fn(*args, session=session, **kwargs)

    return wrapper


@__depends
def query_all(entities, session: Session, **kwargs):
    return session.query(entities).filter_by(**kwargs).all()


@__depends
def query_first(entities, session: Session, **kwargs):
    return session.query(entities).filter_by(**kwargs).first()


@__depends
def insert_many(entities, session: Session, data: List[dict]):
    try:
        instances = [entities(**d) for d in data]
        session.add_all(instances)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@__depends
def insert_one(entity, session: Session, **data):
    try:
        instance = entity(**data)
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


def update_many():
    pass


def update_one():
    pass


@__depends
def upsert(entity, session: Session, data: dict, **kwargs):
    try:
        instance = session.query(entity).filter_by(**kwargs).first()
        if instance:
            for key, value in data.items():
                setattr(instance, key, value)
        else:
            instance = entity(**data)
            session.add(instance)
        session.commit()
        return instance
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@__depends
def delete_many(entities, session: Session, **kwargs):
    try:
        session.query(entities).filter_by(**kwargs).delete(synchronize_session=False)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e


@__depends
def delete_one(entity, session: Session, **kwargs):
    try:
        instance = session.query(entity).filter_by(**kwargs).first()
        if instance:
            session.delete(instance)
            session.commit()
        return instance
    except SQLAlchemyError as e:
        session.rollback()
        raise DatabaseFailure(e) from e
