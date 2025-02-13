from database.connection import DBObject
from typing import Literal, Dict, Any
from model.user import User


class UserRepository:
    @staticmethod
    def find_user(by: Literal["user_uuid", "user_id", "nickname", "email"], value: str) -> User:
        with DBObject.get_instance().session_scope() as session:
            user = session.query(User).filter(
                getattr(User, by) == value).first()
            if user:
                session.expunge(user)

            return user

    @staticmethod
    def create_user(user: User) -> None:
        with DBObject.get_instance().session_scope() as session:
            session.add(user)
            session.flush()
            print(f"'{user.user_uuid}'유저가 성공적으로 생성되었습니다!")

    @staticmethod
    def update_user(user: User, user_data: Dict[str, Any]) -> None:
        with DBObject.get_instance().session_scope() as session:
            exist_user = session.query(User).filter_by(
                user_uuid=user.user_uuid).first()
            if not exist_user:
                raise ValueError("User를 찾을 수 없습니다.")

            for key, value in user_data.items():
                setattr(exist_user, key, value)

            session.flush()
            print(f"'{user.user_uuid}'의 정보가 성공적으로 업데이트 되었습니다.")

    @staticmethod
    def delete_user(user: User) -> None:
        with DBObject.get_instance().session_scope() as session:
            session.delete(user)
            session.flush()
            print(f"'{user.user_uuid}'유저가 성공적으로 제거되었습니다!")

    @staticmethod
    def check_exist_user(by: Literal["user_uuid", "user_id", "nickname", "email"], value: str) -> bool:
        with DBObject.get_instance().session_scope() as session:
            query = session.query(User)
            return query.filter(getattr(User, by) == value).first() is not None
