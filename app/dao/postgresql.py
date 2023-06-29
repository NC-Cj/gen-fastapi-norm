from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from ..env import DATABASE_URL

# Initialize sqlalchemy
__engine = create_engine(DATABASE_URL)
__Session = sessionmaker(bind=__engine)

Base = automap_base()
Base.prepare(autoload_with=__engine)


@contextmanager
def get_session():
    session = __Session()
    try:
        yield session
    finally:
        session.close()
