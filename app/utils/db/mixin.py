from sqlalchemy.orm import declared_attr, Session, aliased

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
    def join_query(cls,
                   related_cls,
                   join_attr,
                   join_type='inner',
                   fields=None,
                   session: Session = None,
                   **kwargs):
        """
        Perform a join query with another class.

        Args:
            related_cls: The related class to join with.
            join_attr: The attribute to join on.
            join_type: The type of join, e.g. 'inner', 'left', 'right', 'outer'.
            fields: The fields to select from the related class.
            session: The SQLAlchemy session.
            **kwargs: Additional filter conditions.

        eg::
            fields = [User.id, User.username, Order.id, Product.name]

            # Join User and Order tables using left join
            query = Mixin.join_query(Order, 'user_id', join_type='left', fields=fields)

            # Join Product table using right join
            query = Mixin.join_query(Product, 'name', join_type='right', fields=fields, session=query.session)

            # Execute the query and retrieve the results
            results = query.all()

        Returns:
            The joined query result.
        """
        if fields is None:
            fields = [related_cls]

        # Create aliases for related_cls to perform multiple joins
        aliases = [aliased(related_cls) for _ in range(len(fields) - 1)]

        qs = session.query(cls)

        # Perform the joins
        for i, alias in enumerate(aliases):
            join_condition = getattr(cls, join_attr) == getattr(alias, join_attr)
            if join_type == 'right':
                qs = qs.join(alias, join_condition, isouter=True)
            elif i == 0:
                qs = qs.join(alias, join_condition)
            else:
                qs = qs.join(alias, join_condition, isouter=(join_type == 'outer'))

        # Apply filter conditions
        for attr, value in kwargs.items():
            if isinstance(value, (list, tuple)):
                qs = qs.filter(getattr(cls, attr).in_(value))

        return qs

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
        session.add_all(data)
        session.commit()

        return (
            [instance.to_dict() for instance in instances]
            if refresh
            else db_result
        )

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
