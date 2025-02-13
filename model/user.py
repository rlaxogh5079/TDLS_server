from sqlalchemy.orm import Mapped, mapped_column
from typing import Dict, Any, Optional
from sqlalchemy import String, TEXT
from pydantic import BaseModel
from datetime import datetime
from model.base import Base
from enum import Enum
import uuid
import jwt
import os


class User(Base):
    __tablename__ = "user"

    user_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    nickname: Mapped[str] = mapped_column(
        String(15), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now())
    avatar_path: Mapped[str | None] = mapped_column(TEXT, default=None)

    def __init__(
        self,
        user_id: str,
        password: str,
        nickname: str,
        email: str,
        user_uuid: str | None = None,
        created_at: datetime | None = None,
    ):
        self.user_uuid = user_uuid
        self.user_id = user_id
        self.password = password
        self.nickname = nickname
        self.email = email
        self.created_at = created_at
        self.avatar_path = None

    def get_attributes(self) -> Dict[str, Any]:
        return {
            "user_uuid": self.user_uuid,
            "user_id": self.user_id,
            "nickname": self.nickname,
            "email": self.email,
            "created_at": self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            "avatar_path": self.avatar_path,
        }


class TokenModel:
    access_token: str
    token_type: str

    def __init__(self, access_token: str, token_type: str):
        self.access_token = access_token
        self.token_type = token_type

    @staticmethod
    def decode_token(access_token: str) -> str:
        acem = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        sk = os.getenv("SECRET_KEY")
        al = os.getenv("ALGORITHM")

        if acem and sk and al:
            payload = jwt.decode(access_token, sk, algorithms=[al])
            user_uuid = payload.get("sub")
            return user_uuid

        else:
            raise FileNotFoundError(
                ".env파일에서 ACCESS_TOKEN_EXPIRE_MINUTES과 SECRET_KEY 환경 변수를 찾을 수 없습니다!"
            )


class CreateUserModel(BaseModel):
    user_id: str
    password: str
    nickname: str
    email: str


class LoginModel(BaseModel):
    user_id: str
    password: str


class ForgotPasswordModel(BaseModel):
    user_id: str
    password: str


class SignoutModel(BaseModel):
    password: str


class UpdateUserModel(BaseModel):
    password: Optional[str] = None
    nickname: Optional[str] = None
    email: Optional[str] = None
    avatar_path: Optional[str] = None


class VerifyErrorCode(Enum):
    SUCCESS = 1  # 인증 성공
    WRONG_VERIFY_CODE = 2  # 인증 코드가 잘못됨
    TIMEOUT = 3  # 타임 아웃
