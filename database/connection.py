from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


class DBObject(object):
    load_dotenv()

    def __init__(self):
        DB_URL = f'mysql+pymysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}'
        self.engine = create_engine(DB_URL)
        self.session = sessionmaker(bind=self.engine)()

    def __del__(self):
        self.engine.dispose()
        self.session.close()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DBObject, cls).__new__(cls)

        return cls.instance
