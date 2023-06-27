from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from ..env import DATABASE_URL

# Initialize sqlalchemy
__engine = create_engine(DATABASE_URL)
__Session = sessionmaker(bind=__engine)

Base = automap_base()
Base.prepare(autoload_with=__engine)


def get_session() -> sessionmaker:
    return __Session
