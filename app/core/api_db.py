from functools import wraps
from typing import Union, List, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, InstrumentedAttribute, selectinload, joinedload

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
def query(
        model: Any,
        session: Session,
        first: bool = False,
        filters: Optional[Dict[str, Union[Any, Dict[str, Any]]]] = None,
        column: Optional[List[str]] = None,
        order_by: Optional[List[str]] = None,
        join: Optional[str] = None
) -> Union[ClauseElement, Any]:
    query_stmt = session.query(model, )
    if join:
        query_stmt = query_stmt.join(join)
    if filters:
        query_stmt = query_stmt.filter(_build_filter(model, filters, join))
    if column:
        columns = [getattr(model, col) for col in column]
        query_stmt = query_stmt.with_entities(*columns)
    if order_by:
        order_bys = [getattr(model, col) for col in order_by]
        query_stmt = query_stmt.order_by(*order_bys)

    return query_stmt.first() if first else query_stmt.all()


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


def _build_filter(
        model: Any,
        filters: Dict[str, Union[Any, Dict[str, Any]]],
        join: Optional[str] = None
) -> ClauseElement:
    clauses = []
    for key, value in filters.items():
        if isinstance(value, dict):
            clause = _build_complex_filter(model, key, value, join)
        else:
            clause = _build_eq_filter(model, key, value, join)
        clauses.append(clause)
    return and_(*clauses)


def _build_eq_filter(model, key, value, join=None):
    if not join:
        return getattr(model, key) == value
    join_model, join_key = join.split('.')
    if model.__name__ == join_model:
        return getattr(model, key) == getattr(model, join_key)
    join_table = getattr(model, join_model)
    return join_table.c[join_key] == value


def _build_operator_filter(
        model: Any,
        key: str,
        operator: str,
        value: Any,
        join: Optional[str] = None
) -> Union[bool, ClauseElement, Any]:
    if operator == 'eq':
        return _build_eq_filter(model, key, value, join)
    elif operator == 'ne':
        return not_(_build_eq_filter(model, key, value, join))
    elif operator == 'lt':
        return getattr(model, key) < value
    elif operator == 'le':
        return getattr(model, key) <= value
    elif operator == 'gt':
        return getattr(model, key) > value
    elif operator == 'ge':
        return getattr(model, key) >= value
    elif operator == 'like':
        return getattr(model, key).like(value)
    elif operator == 'ilike':
        return getattr(model, key).ilike(value)
    elif operator == 'in':
        return getattr(model, key).in_(value)
    elif operator == 'not_in':
        return not_(getattr(model, key).in_(value))
    elif operator == 'is_null':
        return getattr(model, key).is_(None)
    elif operator == 'is_not_null':
        return getattr(model, key).isnot(None)
    elif operator == 'between':
        return getattr(model, key).between(value[0], value[1])
    elif operator == 'not_between':
        return not_(getattr(model, key).between(value[0], value[1]))
    elif operator == 'contains':
        return getattr(model, key).contains(value)
    elif operator == 'not_contains':
        return not_(getattr(model, key).contains(value))
    elif operator == 'startswith':
        return getattr(model, key).startswith(value)
    elif operator == 'endswith':
        return getattr(model, key).endswith(value)
    elif operator == 'or':
        return _build_or_filter(model, key, value)
    else:
        raise ValueError(f'Unsupported operator: {operator}')


def _build_or_filter(
        model: Any,
        key: str,
        value: List[Dict[str, Any]],
        join: Optional[str] = None
) -> ClauseElement:
    sub_clauses = []
    for sub_filters in value:
        sub_clause = _build_complex_filter(model, key, sub_filters, join)
        sub_clauses.append(sub_clause)
    return or_(*sub_clauses)


def _build_complex_filter(
        model: Any,
        key: str,
        filters: Dict[str, Any],
        join: Optional[str] = None
) -> ClauseElement:
    clauses = []
    for op, value in filters.items():
        clause = _build_operator_filter(model, key, op, value, join)
        clauses.append(clause)
    return and_(*clauses)
