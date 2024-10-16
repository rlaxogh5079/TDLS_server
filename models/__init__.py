from database.connection import DBObject
from .friend import Friend
from .user import User

DBObject()

for table in [User, Friend]:
    table.__table__.create(bind=DBObject.instance.engine, checkfirst=True)
