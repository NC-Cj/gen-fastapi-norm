from sqlalchemy import text, Executable
from sqlalchemy.orm import declarative_base, Session

from .mixin import Mixin
from .session import auto_session
from ..types.converter_type import db_result

Base = declarative_base(cls=Mixin)


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
        return db_result

    return result


@auto_session
def execute_custom_func(func_name: str,
                        params: dict = None,
                        session: Session = None):
    statement = text(f"SELECT {func_name}({', '.join(params)})")
    return session.execute(statement)


@auto_session
def conn_execute(statement: Executable,
                 params: dict = None,
                 session: Session = None):
    conn = session.connection()
    return conn.execute(statement, params)
