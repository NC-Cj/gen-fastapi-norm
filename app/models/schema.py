"""
I definitely do not recommend declaring the table structure of the data layer in a web project,
and I recommend using a third-party tool such as prisma orm to do so Your data sheet.

Here we can reflect the table structure in the database to allow you to continue using the Session operation

Or you can do it the way you like, and what's clear here is that the table structure is reflected,
regardless of whether you declare it in the code or not
"""
from sqlalchemy import Table

from ..dao.db import engine
from ..utils.db.db_helpers import Base


# Define table classes for mapping
class Boss(Base):
    __table__ = Table('boss', Base.metadata, autoload_with=engine)

    # You can add custom methods based on reflected model classes
