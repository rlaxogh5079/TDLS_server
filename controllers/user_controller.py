from services.user_service import (
    create_user,
    read_user_by_uuid,
    update_user_by_uuid,
    delete_user_by_uuid,
    convert_id_to_uuid,
    check_exist_user,
    login_service,
    update_avatar_service,
    send_email_service,
    verify_email_service,
)
from models.user import (
    CreateUserModel,
    ForgotPasswordModel,
    SignoutModel,
    User,
    ExistErrorCode,
    VerifyErrorCode,
)
from models.response import (
    ResponseStatusCode,
    Detail,
    TDLSException,
)
from fastapi.security import OAuth2PasswordRequestForm
from database.connection import DBObject
from models.response import TokenModel
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
            create_user(
                db.session,
                user_info.user_id,
                hashed_password,
                user_info.nickname,
                user_info.email,
            )

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

    except Exception as e:
        raise TDLSException(str(e))


def signout(db: DBObject, user_info: SignoutModel) -> Tuple[ResponseStatusCode, Detail]:
    try:
        status_code, detail = login(
            db,
            OAuth2PasswordRequestForm(
                username=user_info.user_id, password=user_info.password
            ),
        )
        if status_code != ResponseStatusCode.SUCCESS:
            return (status_code, detail)  # type: ignore

        delete_user_by_uuid(db.session, user_info.access_token)
        return (ResponseStatusCode.SUCCESS, Detail(None))

    except Exception as e:
        raise TDLSException(str(e))


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
        raise TDLSException(str(e))


def forgot_password(
    db: DBObject, user_info: ForgotPasswordModel
) -> Tuple[ResponseStatusCode, Detail]:
    user_uuid = convert_id_to_uuid(db.session, user_info.user_id)
    if user_uuid is None:
        return (ResponseStatusCode.FAIL, Detail("아이디를 확인해 주세요"))

    update_user_by_uuid(
        db.session, user_uuid=user_uuid, option="password", value=user_info.password
    )
    return (ResponseStatusCode.SUCCESS, Detail(None))


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
        user_uuid = TokenModel.decode_token(access_token)
        result = read_user_by_uuid(db.session, user_uuid)
        if result:
            return (ResponseStatusCode.SUCCESS, result)

        else:
            return (ResponseStatusCode.NOT_FOUND, Detail("User not founded"))

    except Exception as e:
        raise TDLSException(str(e))


def update_avatar(
    db: DBObject, access_token: str, file: bytes | None = None
) -> Tuple[ResponseStatusCode, Detail]:
    try:
        update_avatar_service(db.session, access_token, file)
        return (ResponseStatusCode.SUCCESS, Detail(None))

    except Exception as e:
        raise TDLSException(str(e))


def send_email(email: str) -> Tuple[ResponseStatusCode, Detail]:
    try:
        send_email_service(email)
        return (ResponseStatusCode.SUCCESS, Detail(None))

    except Exception as e:
        raise TDLSException(str(e))


def verify_email(email: str, verify_code: str) -> Tuple[ResponseStatusCode, Detail]:
    try:
        return {
            VerifyErrorCode.SUCCESS: (ResponseStatusCode.SUCCESS, Detail(None)),
            VerifyErrorCode.WRONG_VERIFY_CODE: (
                ResponseStatusCode.FAIL,
                Detail("인증번호가 잘못되었습니다."),
            ),
            VerifyErrorCode.TIMEOUT: (
                ResponseStatusCode.TIME_OUT,
                Detail("인증 시간이 초과되었습니다."),
            ),
        }[verify_email_service(email, verify_code)]

    except Exception as e:
        raise TDLSException(str(e))
