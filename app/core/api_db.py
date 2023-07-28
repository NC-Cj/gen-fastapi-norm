from functools import wraps
from typing import Union, List, Type

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, defer, joinedload, load_only

from ..dao.postgresql import get_session
from ..pkg.error import DatabaseFailure, InvalidValueError
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
def execute_sql(session: Session, sql):
    return session.execute(text(sql))


@with_db_session
def simple_query(model,
                 session: Session,
                 first: bool = False,
                 includes: List[str] = None,
                 excludes: List[str] = None,
                 **kwargs):
    """
    Returns query results from the given model.

    :param model: SQLAlchemy model to query.
    :param session: SQLAlchemy Session object.
    :param first: If True, returns only the first result. Otherwise, returns all results.
    :param includes: List of column names to include in the results.
    :param excludes: List of column names to exclude from the results.
    :param kwargs: Filter arguments to apply to the query.
    :return: Query results.
    """
    qs = session.query(model)

    if kwargs:
        qs = qs.filter_by(**kwargs)

    # if includes and excludes:
    #     raise ValueError("Cannot use both includes and exclude")

    if includes:
        qs = qs.options(load_only(*includes))

    if excludes:
        qs = qs.options(defer(*excludes))

    return qs.first() if first else qs.all()


@with_db_session
def join_query(model,
               session: Session,
               limit=None,
               offset=None,
               order_by: List[tuple] = None,
               joins: List[tuple] = None,
               add_entitys: List[Type] = None,
               includes: List[str] = None,
               excludes: List[str] = None,
               **kwargs):
    qs = session.query(model)

    for join in joins:
        qs = qs.join(*join)

    qs = qs.filter_by(**kwargs)

    if add_entitys:
        for entity in add_entitys:
            qs = qs.add_entity(entity)
    if order_by:
        qs = qs.order_by(*order_by)
    if limit is not None:
        qs = qs.limit(limit)
    if offset is not None:
        qs = qs.offset(offset)
    if includes:
        qs = qs.options(load_only(*includes))
    if excludes:
        qs = qs.options(defer(*excludes))

    return qs.all()


@with_db_session
def query(model,
          session: Session,
          first=False,
          join_load: Optional[List[InstrumentedAttribute]] = None,
          includes: Optional[List[InstrumentedAttribute]] = None,
          excludes: Optional[List[InstrumentedAttribute]] = None,
          **kwargs) -> Union[list, str]:
    qs = session.query(model).filter_by(**kwargs)

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
def insert(model,
           session: Session,
           data: Union[list, dict],
           refresh=False) -> Union[list, str]:
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
def delete(model,
           session: Session,
           **kwargs) -> str:
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
def upsert(model,
           session: Session,
           data: Union[list, dict],
           unique_columns: list,
           update_columns=None,
           refresh=False) -> Union[list, str]:
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
def update(model,
           session: Session,
           data: Union[list, dict],
           refresh=False,
           **kwargs) -> Union[list, str]:
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
