from .user import User
from database.connection import DBObject

DBObject()

for table in [User]:
    table.__table__.create(bind=DBObject.instance.engine, checkfirst=True)
