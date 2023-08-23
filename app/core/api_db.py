from contextlib import contextmanager

from sqlalchemy import text
from sqlalchemy.orm import declared_attr, declarative_base, Session

from .converter_type import ResultConverter
from ..dao.db import my_session
from ..pkg.error import DatabaseFailure

OK = "ok"


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


@auto_session
def execute_raw_sql(sql: str,
                    params=None,
                    commit=False,
                    session: Session = None):
    statement = text(sql)
    if params is None:
        result = session.execute(statement)
    else:
        result = session.execute(statement, params)

    if commit:
        session.commit()
        return OK

    return result


@auto_session
def execute_custom_func(func_name: str,
                        params=None,
                        session: Session = None):
    statement = text(f"SELECT {func_name}({', '.join(params)})")
    return session.execute(statement)


class Mixin:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def simple_query_with_filters(cls,
                                  kwargs,
                                  session):
        """
        Construct a query object, is simple filter that supports `equal` to and `in`
        """
        qs = session.query(cls)

        for attr, value in kwargs.items():
            if isinstance(value, (list, tuple)):
                qs = qs.filter(getattr(cls, attr).in_(value))
            else:
                qs = qs.filter(getattr(cls, attr) == value)

        return qs

    @classmethod
    @auto_session
    def filter(cls,
               first=False,
               result_converter: ResultConverter = None,
               session: Session = None,
               **kwargs):
        """
        Simple filter that supports `equal` to and `in`
        """
        qs = cls.simple_query_with_filters(kwargs, session)
        result = qs.first() if first else qs.all()

        return result_converter.convert(result) if result_converter else result

    @classmethod
    @auto_session
    def save_many(cls,
                  data,
                  refresh: bool = False,
                  session: Session = None):
        instances = list(data)
        session.bulk_save_objects(data)
        session.commit()

        if refresh:
            session.refresh(instances)

        return instances if refresh else "OK"

    @classmethod
    @auto_session
    def delete(cls,
               refresh: bool = False,
               session: Session = None,
               **kwargs):
        qs = cls.simple_query_with_filters(kwargs, session)
        deleted_instances = qs.delete(synchronize_session=False)
        session.commit()
        return deleted_instances if refresh else OK

    @classmethod
    @auto_session
    def update(cls,
               data,
               refresh: bool = False,
               session: Session = None,
               **kwargs):
        qs = cls.simple_query_with_filters(kwargs, session)
        instances = qs.update(data, synchronize_session=False)
        session.commit()
        return instances if refresh else OK

    @classmethod
    @auto_session
    def upsert(cls,
               update_dict,
               refresh: bool = False,
               session: Session = None,
               **kwargs):
        qs = cls.simple_query_with_filters(kwargs, session)
        existing_instances = qs.all()

        for instance in existing_instances:
            instance.update(session, update_dict)

        non_existing_values = set(kwargs.values()) - {
            getattr(instance, attr)
            for instance in existing_instances
            for attr in kwargs
        }
        new_instances = [cls(**dict(zip(kwargs.keys(), values)), **update_dict) for values in non_existing_values]
        session.add_all(new_instances)
        session.commit()
        return existing_instances + new_instances if refresh else OK

    @auto_session
    def save(self,
             session: Session = None,
             refresh: bool = False):
        session.add(self)
        session.commit()

        if refresh:
            session.refresh(self)
            return self
        return OK

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    # @auto_session
    # def query(self,
    #           result_converter: ResultConverter = None,
    #           session: Session = None):
    #     print(session)
    #
    #     result = session.query(self).all()
    #     print(result)
    #
    #     return result_converter.convert(result) if result_converter else result


Base = declarative_base(cls=Mixin)
