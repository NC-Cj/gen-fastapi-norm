from functools import wraps
from typing import Union, List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, InstrumentedAttribute, load_only, defer, joinedload

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
def simple_query(
        model,
        session: Session,
        first=False,
        includes: Optional[List[InstrumentedAttribute]] = None,
        excludes: Optional[List[InstrumentedAttribute]] = None,
        **kwargs
):
    qs = session.query(model).filter_by(**kwargs)

    if includes:
        qs = qs.options(load_only(*includes))
    if excludes:
        qs = qs.options(defer(*excludes))

    return qs.first() if first else qs.all()


@with_db_session
def query(
        model,
        session: Session,
        first=False,
        joins: Optional[List[Union[InstrumentedAttribute, tuple]]] = None,
        join_load: Optional[List[InstrumentedAttribute]] = None,
        includes: Optional[List[InstrumentedAttribute]] = None,
        excludes: Optional[List[InstrumentedAttribute]] = None,
        **kwargs
):
    qs = session.query(model)

    # if joins:
    #     for item in joins:
    #         qs = qs.join(*item) if isinstance(item, tuple) else qs.join(item)

    qs = qs.filter_by(**kwargs)

    if join_load:
        for item in join_load:
            qs = qs.options(joinedload(item))

    if includes:
        qs = qs.options(load_only(*includes))

    if excludes:
        qs = qs.options(defer(*excludes))

    print(qs)
    return qs.first() if first else qs.all()


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
        qs = session.query(model)
        for k, v in kwargs.items():
            if isinstance(v, (list, tuple)):
                qs = qs.filter(getattr(model, k).in_(v))
            else:
                qs = qs.filter_by(**{k: v})

        qs.delete(synchronize_session=False)
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
