from functools import wraps
from typing import Union, List, Type, Any

from sqlalchemy import text
from sqlalchemy.orm import Session, defer, load_only

from ..dao.postgresql import get_session
from ..pkg.error import DatabaseFailure, UnsupportedDataTypeError

OK = "ok"


def query_with_filters(kwargs, model, session):
    qs = session.query(model)
    for k, v in kwargs.items():
        if isinstance(v, (list, tuple)):
            qs = qs.filter(getattr(model, k).in_(v))
        else:
            qs = qs.filter_by(**{k: v})

    return qs


def model_to_dict(data: Any) -> Any:
    if isinstance(data, list):
        return [model_to_dict(item) for item in data]
    elif isinstance(data, dict):
        return data
    elif hasattr(data, 'dict'):
        return data.dict()
    else:
        raise UnsupportedDataTypeError(f'Unsupported data type: {type(data)}')


def with_db_session(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not kwargs.get("session"):
            with get_session() as session:
                try:
                    if kwargs.get("data"):
                        kwargs["data"] = model_to_dict(kwargs.get("data"))

                    return fn(*args, session=session, **kwargs)
                except Exception as e:
                    session.rollback()
                    raise DatabaseFailure(e) from e

    return wrapper


@with_db_session
def execute(stmt, commit, session: Session):
    if commit:
        session.execute(stmt)
        session.commit()
        return OK
    return session.execute(stmt)


@with_db_session
def execute_sql(sql, commit, session: Session):
    return execute(text(sql), commit, session)


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
def insert(model,
           session: Session,
           data: Union[list, dict],
           refresh=False) -> Union[list, str]:
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

    if refresh:
        if not isinstance(instance, list):
            session.refresh(instance)
        return instance
    return OK


@with_db_session
def delete(model,
           session: Session,
           **kwargs) -> str:
    qs = query_with_filters(kwargs, model, session)
    qs.delete(synchronize_session=False)
    session.commit()
    return OK


@with_db_session
def upsert(model,
           session: Session,
           data: Union[list, dict],
           unique_columns: list,
           update_columns=None,
           refresh=False) -> Union[list, str]:
    instances = []
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
    return instances if refresh else OK


@with_db_session
def update(model,
           session: Session,
           data: Union[list, dict],
           refresh=False,
           **kwargs) -> Union[list, str]:
    qs = query_with_filters(kwargs, model, session)

    if isinstance(data, (dict, list)):
        qs.update(data, synchronize_session=False)
    else:
        raise TypeError("argument: data, must be a dict or a list of dicts")

    session.commit()
    return qs.all() if refresh else OK
