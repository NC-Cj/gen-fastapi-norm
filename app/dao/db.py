from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..env import DATABASE_URL

# Initialize sqlalchemy
engine = create_engine(DATABASE_URL)
my_session = sessionmaker(bind=engine)
