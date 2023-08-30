from sqlalchemy.orm import declared_attr, Session

from .session import auto_session
from ...utils.types.converter_type import ResultConverter, db_result


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
        """Simple filter that supports `equal` to and `in`

        e.g.::

            res = YourClass.filter(first=True, id=1, name=variable)
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
        """Insert multiple instance data at once.
        e.g.::
            data = [
                YourClass(name=variable, age=12),
                YourClass(name=variable, age=12)
            ]
            res = YourClass.save_many(data)
        """
        instances = list(data)
        session.bulk_save_objects(data)
        session.commit()

        if refresh:
            session.refresh(instances)

        return instances if refresh else db_result

    @classmethod
    @auto_session
    def delete(cls,
               refresh: bool = False,
               session: Session = None,
               **kwargs):
        """Delete a row of data.
        e.g.::
            res = YourClass.delete(id=1)
        """
        qs = cls.simple_query_with_filters(kwargs, session)
        deleted_instances = qs.delete(synchronize_session=False)
        session.commit()
        return deleted_instances if refresh else db_result

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
        return instances if refresh else db_result

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
        return existing_instances + new_instances if refresh else db_result

    @auto_session
    def save(self,
             session: Session = None,
             refresh: bool = False):
        """Insert a row of instance data
        e.g.::

            res = YourClass(name=variable, age=12).save()
        """
        session.add(self)
        session.commit()

        if refresh:
            session.refresh(self)
            return self
        return db_result

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
