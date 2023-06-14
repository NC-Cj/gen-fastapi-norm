"""
I definitely do not recommend declaring the table structure of the data layer in a web project,
and I recommend using a third-party tool such as prisma orm to do so Your data sheet.

Here we can reflect the table structure in the database to allow you to continue using the Session operation

Or you can do it the way you like, and what's clear here is that the table structure is reflected,
regardless of whether you declare it in the code or not
"""

from sqlalchemy.ext.automap import automap_base

from ..dao.postgresql import engine

__Base = automap_base()
__Base.prepare(autoload_with=engine)

User = __Base.classes.user
