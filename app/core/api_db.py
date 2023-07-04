from functools import wraps
from typing import Union

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..dao.postgresql import get_session
from ..pkg.error import DatabaseFailure
from ..pkg.tools import model_to_dict


def with_db_session(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with get_session() as session:
            if kwargs.get("data"):
                kwargs["data"] = model_to_dict(kwargs.get("data"))

            return fn(*args, session=session, **kwargs)

    return wrapper


@with_db_session
def query_all(model, session: Session, **kwargs):
    return session.query(model).filter_by(**kwargs).all()


@with_db_session
def query_first(model, session: Session, **kwargs):
    return session.query(model).filter_by(**kwargs).first()


@with_db_session
def insert(model, session: Session, data: Union[list, dict], refresh=False):
    try:
        if isinstance(data, dict):
            instance = model(**data)
            session.add(instance)
            session.commit()
        elif isinstance(data, list):
            instance = [model(**d) for d in data]
            session.bulk_save_objects(instance)
            session.commit()
        else:
            raise TypeError("argument: data, must be a dict or a list of dicts")
    except IntegrityError as e:
        session.rollback()
        raise DatabaseFailure(e) from e
    else:
        if refresh:
            if not isinstance(instance, list):
                session.refresh(instance)
            return instance
        return "ok"


@with_db_session
def delete(model, session: Session, **kwargs) -> str:
    try:
        query = session.query(model)
        for k, v in kwargs.items():
            if isinstance(v, (list, tuple)):
                query = query.filter(getattr(model, k).in_(v))
            else:
                query = query.filter_by(**{k: v})

        query.delete(synchronize_session=False)
        session.commit()
    except Exception as e:
        session.rollback()
        raise DatabaseFailure(e) from e
    else:
        return "ok"


@with_db_session
def upsert(model, session: Session, data: Union[list, dict], unique_columns: list, update_columns=None, refresh=False):
    instances = []
    try:
        if isinstance(data, dict):
            data = [data]

        for item in data:
            unique_filter = {key: item[key] for key in unique_columns}
            instance = session.query(model).filter_by(**unique_filter).first()

            if instance:
                if update_columns:
                    update_data = {key: item[key] for key in update_columns}
                else:
                    update_data = item

                for key, value in update_data.items():
                    setattr(instance, key, value)

            else:
                instance = model(**item)
                session.add(instance)
            instances.append(instance)

        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise DatabaseFailure(e) from e
    else:
        return instances if refresh else "ok"


@with_db_session
def update(model, session: Session, data: Union[list, dict], refresh=False, **kwargs):
    try:
        instance = session.query(model)
        for k, v in kwargs.items():
            if isinstance(v, (list, tuple)):
                instance = instance.filter(getattr(model, k).in_(v))
            else:
                instance = instance.filter_by(**{k: v})

        if isinstance(data, (dict, list)):
            instance.update(data, synchronize_session=False)
        else:
            raise TypeError("argument: data, must be a dict or a list of dicts")
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise DatabaseFailure(e) from e
    else:
        return instance.all() if refresh else "ok"
