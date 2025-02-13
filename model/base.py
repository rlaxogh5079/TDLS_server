from sqlalchemy.ext.declarative import declarative_base
from database.connection import DBObject
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

Base.metadata.create_all(bind=DBObject.get_instance().engine)
