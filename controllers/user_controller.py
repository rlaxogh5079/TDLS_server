from services.user_service import (
    create_user,
    read_user_by_uuid,
    update_user_by_uuid,
    delete_user_by_uuid,
    convert_id_to_uuid,
    check_exist_user,
    login_service,
    update_avatar_service,
)
from models.user import CreateUserModel, ForgotPasswordModel, SignoutModel, User
from models.response import ResponseStatusCode, Detail, ExistErrorCode
from fastapi.security import OAuth2PasswordRequestForm
from database.connection import DBObject
from typing import Tuple
import bcrypt


def signup(
    db: DBObject, user_info: CreateUserModel
) -> Tuple[ResponseStatusCode, Detail]:
    try:
        exist_code = check_exist_user(
            se=db.session,
            user_id=user_info.user_id,
            nickname=user_info.nickname,
            email=user_info.nickname,
        )

        if exist_code == ExistErrorCode.USEFUL:
            hashed_password = bcrypt.hashpw(
                user_info.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            result = create_user(
                db.session,
                user_info.user_id,
                hashed_password,
                user_info.nickname,
                user_info.email,
            )

            if result:
                return (ResponseStatusCode.SUCCESS, Detail(None))

            else:
                return (ResponseStatusCode.FAIL, Detail("회원가입에 실패하였습니다!"))

        else:
            detail = Detail(None)
            if exist_code == ExistErrorCode.USERID:
                detail = Detail("유저 아이디가 중복되었습니다!")

            elif exist_code == ExistErrorCode.NICKNAME:
                detail = Detail("닉네임이 중복되었습니다!")

            elif exist_code == ExistErrorCode.EMAIL:
                detail = Detail("이메일이 중복되었습니다!")

            return (ResponseStatusCode.CONFLICT, detail)

    except Exception as e:
        return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))


def signout(db: DBObject, user_info: SignoutModel) -> Tuple[ResponseStatusCode, Detail]:
    try:
        status_code, detail = login(db, OAuth2PasswordRequestForm(username=user_info.user_id, password=user_info.password))  # type: ignore
        if status_code != ResponseStatusCode.SUCCESS:
            return (status_code, detail)  # type: ignore

        result = delete_user_by_uuid(db.session, user_info.access_token)
        if result:
            return (ResponseStatusCode.SUCCESS, Detail(None))

        else:
            return (ResponseStatusCode.FAIL, Detail("계정 제거에 실패하였습니다."))

    except Exception as e:
        return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))


def login(
    db: DBObject, user_info: OAuth2PasswordRequestForm
) -> Tuple[ResponseStatusCode, Detail | str]:
    try:
        token = login_service(db.session, user_info.username, user_info.password)
        if token is None:
            return (
                ResponseStatusCode.FAIL,
                Detail("아이디 또는 비밀번호가 잘못 입력되었습니다!"),
            )

        return (ResponseStatusCode.SUCCESS, token.access_token)

    except Exception as e:
        return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))


def forgot_password(
    db: DBObject, user_info: ForgotPasswordModel
) -> Tuple[ResponseStatusCode, Detail]:
    user_uuid = convert_id_to_uuid(db.session, user_info.user_id)
    if user_uuid is None:
        return (ResponseStatusCode.FAIL, Detail("아이디를 확인해 주세요"))

    result = update_user_by_uuid(
        db.session, user_uuid=user_uuid, option="password", value=user_info.password
    )

    if result:
        return (ResponseStatusCode.SUCCESS, Detail(None))

    return (
        ResponseStatusCode.INTERNAL_SERVER_ERROR,
        Detail("비밀번호 변경에 실패하였습니다."),
    )


def check_duplicate(
    db: DBObject,
    user_id: str | None = None,
    nickname: str | None = None,
    email: str | None = None,
) -> Tuple[ResponseStatusCode, Detail]:
    exist_code = check_exist_user(db.session, user_id, nickname, email)

    if exist_code == ExistErrorCode.USEFUL:
        return (ResponseStatusCode.SUCCESS, Detail(None))

    else:
        detail = Detail(None)
        if exist_code == ExistErrorCode.USERID:
            detail = Detail("유저 아이디가 중복되었습니다!")

        elif exist_code == ExistErrorCode.NICKNAME:
            detail = Detail("닉네임이 중복되었습니다!")

        elif exist_code == ExistErrorCode.EMAIL:
            detail = Detail("이메일이 중복되었습니다!")

        return (ResponseStatusCode.CONFLICT, detail)


def get_profile(
    db: DBObject, access_token: str
) -> Tuple[ResponseStatusCode, Detail | User]:
    try:
        result = read_user_by_uuid(db.session, access_token)
        if result:
            return (ResponseStatusCode.SUCCESS, result)

        else:
            return (ResponseStatusCode.NOT_FOUND, Detail("User not founded"))

    except Exception as e:
        return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))


def update_avatar(
    db: DBObject, access_token: str, file: bytes | None = None
) -> Tuple[ResponseStatusCode, Detail]:

    try:
        if update_avatar_service(db.session, access_token, file):
            return (ResponseStatusCode.SUCCESS, Detail(None))

        else:
            return (ResponseStatusCode.FAIL, Detail("Failed to update avatar"))

    except Exception as e:
        return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))
