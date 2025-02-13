from model.user import VerifyErrorCode, TokenModel, CreateUserModel, User
from repository.user_repository import UserRepository
from model.response import ResponseStatusCode, Detail
from fastapi.security import OAuth2PasswordBearer
from email.mime.multipart import MIMEMultipart
from service.auth_service import AuthService
from email.mime.text import MIMEText
from datetime import datetime
from fastapi import Depends
from random import randint
from typing import Tuple
import traceback
import logging
import smtplib
import os

email_session = {}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


class UserService:
    @staticmethod
    def login(user_id: str, password: str) -> Tuple[ResponseStatusCode, Detail | TokenModel]:
        try:
            user = AuthService.authenticate_user(user_id, password)
            if not user:
                return (ResponseStatusCode.NOT_FOUND, Detail(f"'{user_id}'라는 유저 아이디를 가진 유저를 찾을 수 없습니다."))

            access_token = AuthService.create_access_token(
                data={"sub": user.user_uuid})

            return (ResponseStatusCode.SUCCESS, TokenModel(access_token=access_token, token_type="bearer"))

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    def signup(user: CreateUserModel) -> Tuple[ResponseStatusCode, Detail | None]:
        try:
            db_user = User(user.user_id, user.password,
                           user.nickname, user.email)
            if UserRepository.check_exist_user("user_id", db_user.user_id):
                return (ResponseStatusCode.CONFLICT, Detail(f"'{db_user.user_id}'라는 유저 아이디를 가진 유저가 이미 존재합니다."))

            if UserRepository.check_exist_user("nickname", db_user.nickname):
                return (ResponseStatusCode.CONFLICT, Detail(f"'{db_user.nickname}'라는 닉네임을 가진 유저가 이미 존재합니다."))

            if UserRepository.check_exist_user("email", db_user.email):
                return (ResponseStatusCode.CONFLICT, Detail(f"'{db_user.email}'라는 이메일을 가진 유저가 이미 존재합니다."))

            UserRepository.create_user(db_user)
            return (ResponseStatusCode.CREATED, None)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme)) -> Tuple[ResponseStatusCode, Detail | User]:
        try:
            user_uuid = TokenModel.decode_token(token)
            if not user_uuid:
                return (ResponseStatusCode.FAIL, Detail(f"'{token}'은 유요한 토큰이 아닙니다."))

            user = UserRepository.find_user(by="user_uuid", value=user_uuid)
            if not user:
                return (ResponseStatusCode.NOT_FOUND, Detail(f"'{token}'을 할당받은 유저를 찾을 수 없습니다."))

            return (ResponseStatusCode.SUCCESS, user)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    def update_user(user: User, password: str | None = None, nickname: str | None = None, email: str | None = None, avatar_path: str | None = None) -> Tuple[ResponseStatusCode, Detail | User]:
        try:
            user_data = {}

            if password:
                user_data["password"] = password
            if nickname:
                user_data["nickname"] = nickname
            if email:
                user_data["email"] = email
            if avatar_path:
                user_data["avatar_path"] = avatar_path

            UserRepository.update_user(user, user_data)
            user = UserRepository.find_user("user_uuid", user.user_uuid)

            return (ResponseStatusCode.SUCCESS, user)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    def delete_user(user: User, password: str) -> Tuple[ResponseStatusCode, Detail | None]:
        try:
            status_code, result = UserService.login(user.user_id, password)
            if isinstance(result, Detail):
                return (status_code, result)

            UserRepository.delete_user(user)
            return (ResponseStatusCode.SUCCESS, None)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    def send_email_service(email: str) -> Tuple[ResponseStatusCode, Detail | None]:
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = "TDLS 인증번호 요청"
            message["From"] = str(os.getenv("SENDER"))
            message["To"] = email
            print(message)
            print(os.getenv("APP_PASSWORD"))
            email_session[f"{email}-verify-code"] = str(
                randint(10**4, 10**6 - 1)
            ).rjust(6, "0")
            text = f"<html><body><div>인증 코드: {
                email_session[f'{email}-verify-code']}</div></body></html>"
            part2 = MIMEText(text, "html")
            message.attach(part2)
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(str(os.getenv("SENDER")),
                             str(os.getenv("APP_PASSWORD")))
                server.sendmail(str(os.getenv("SENDER")),
                                email, message.as_string())

            email_session[f"{email}-start-time"] = datetime.now().strftime(
                "%Y/%m/%d %H:%M:%S"
            )

            return (ResponseStatusCode.SUCCESS, None)

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            return (ResponseStatusCode.INTERNAL_SERVER_ERROR, Detail(str(e)))

    @staticmethod
    def verify_email_service(email: str, verify_code: str) -> VerifyErrorCode:
        try:
            if (
                f"{email}-verify-code" not in email_session.keys()
                or (
                    datetime.now()
                    - datetime.strptime(
                        email_session[f"{
                            email}-start-time"], "%Y/%m/%d %H:%M:%S"
                    )
                ).total_seconds()
                >= 300
            ):
                return VerifyErrorCode.TIMEOUT

            elif verify_code != email_session[f"{email}-verify-code"]:
                return VerifyErrorCode.WRONG_VERIFY_CODE

            return VerifyErrorCode.SUCCESS

        except Exception as e:
            logging.error(
                f"{e}: {''.join(traceback.format_exception(
                    None, e, e.__traceback__))}"
            )
            raise e
