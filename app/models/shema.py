from sqlalchemy.ext.automap import automap_base

from ..dao.postgresql import engine

__Base = automap_base()
__Base.prepare(autoload_with=engine)

User = __Base.classes.user
