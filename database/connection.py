from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import urllib
import os


class DBObject(object):
    _instance = None

    def __init__(self):
        """__init__ 호출 방지"""
        raise RuntimeError("Use DBObject.get_instance() instead")

    @classmethod
    def get_instance(cls):
        """DBObject의 싱글턴 인스턴스를 반환"""
        if cls._instance is None:
            DB_USER = os.getenv("DB_USER")
            DB_PASSWORD = os.getenv("DB_PASSWORD")
            DB_HOST = os.getenv("DB_HOST")
            DB_PORT = os.getenv("DB_PORT")
            DB_NAME = os.getenv("DB_NAME")

            if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
                raise Exception("환경 변수가 올바르게 설정되지 않았습니다. .env 파일을 확인하세요.")

            try:
                DB_URL = (
                    f"mysql+pymysql://{urllib.parse.quote(DB_USER)}:"
                    f"{urllib.parse.quote(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/"
                    f"{urllib.parse.quote(DB_NAME)}"
                )

                cls._instance = object.__new__(cls)
                cls._instance.engine = create_engine(DB_URL)
                cls._instance.Session = sessionmaker(bind=cls._instance.engine)

            except Exception as e:
                print(f"데이터베이스 연결 오류: {e}")
                raise Exception("데이터베이스 연결에 실패했습니다. 환경 변수를 확인하세요.")

        return cls._instance

    def get_session(self):
        return self.Session()

    @contextmanager
    def session_scope(self):
        session = self.get_session()
        try:
            yield session
            session.commit()

        except Exception as e:
            session.rollback()
            print(f"SQL에서 오류가 발생하였습니다: {e}")
            raise

        finally:
            session.close()
