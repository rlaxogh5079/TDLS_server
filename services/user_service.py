from models.response import ExistErrorCode, TokenModel
from sqlalchemy.orm.session import Session
from models.user import User
from typing import Literal
import traceback
import logging
import bcrypt


def create_user(
    se: Session, user_id: str, password: str, nickname: str, email: str
) -> bool:
    try:
        user = User(user_id=user_id, password=password, nickname=nickname, email=email)
        se.add(user)
        se.commit()
        se.refresh(user)
        return True

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        return False


def read_user_by_uuid(se: Session, access_token: str) -> User | None:
    try:
        user_uuid = TokenModel.decode_token(access_token)
        result = se.query(User).filter_by(user_uuid=user_uuid).first()
        return result

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        raise e


def update_user_by_uuid(
    se: Session,
    user_uuid: str,
    option: Literal["password", "nickname", "email"],
    value: str,
) -> bool:
    try:
        se.query(User).filter_by(user_uuid=user_uuid).update({option: value})
        se.commit()
        return True

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        return False


def delete_user_by_uuid(se: Session, access_token: str) -> bool:
    try:
        user_uuid = TokenModel.decode_token(access_token)
        se.query(User).filter_by(user_uuid=user_uuid).delete()
        se.commit()
        return True

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        return False


def convert_id_to_uuid(se: Session, user_id: str) -> str | None:
    try:
        result = se.query(User.user_uuid).filter_by(user_id=user_id).first()
        if result:
            return result[0]

        return None

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        raise e


def check_exist_user(
    se: Session,
    user_id: str | None = None,
    nickname: str | None = None,
    email: str | None = None,
) -> ExistErrorCode:
    query = se.query(User)

    if user_id:
        result = query.filter_by(user_id=user_id).first()
        if result is not None:
            return ExistErrorCode.USERID

    if nickname:
        result = query.filter_by(nickname=nickname).first()
        if result is not None:
            return ExistErrorCode.NICKNAME

    if email:
        result = query.filter_by(email=email).first()
        if result is not None:
            return ExistErrorCode.EMAIL

    return ExistErrorCode.USEFUL


def login_service(se: Session, user_id: str, password: str) -> TokenModel | None:
    try:
        load_password = se.query(User.password).filter_by(user_id=user_id).first()
        if load_password is None:
            return None

        if bcrypt.checkpw(password.encode("utf-8"), load_password[0].encode("utf-8")):
            user_uuid = se.query(User.user_uuid).filter_by(user_id=user_id).first()
            if user_uuid is None:
                return None

            return TokenModel(user_uuid=user_uuid[0])

        else:
            print("login failed")
            return None

    except Exception as e:
        logging.error(
            f"{e}: {''.join(traceback.format_exception(None, e, e.__traceback__))}"
        )
        raise e
