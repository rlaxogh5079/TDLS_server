from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timedelta
from pydantic import BaseModel
from sqlalchemy import String
from typing import Dict, Any
from base64 import b64decode
from models.base import Base
import uuid
import jwt
import os


class User(Base):
    __tablename__ = "User"

    user_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    nickname: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())

    def __init__(
        self,
        user_id: str,
        password: str,
        nickname: str,
        email: str,
        user_uuid: str | None = None,
        created_at: datetime | None = None,
    ):
        self.user_uuid = user_uuid if user_uuid else str(uuid.uuid4())
        self.user_id = user_id
        self.password = password
        self.nickname = nickname
        self.email = email
        self.created_at = created_at if created_at else datetime.now()

    def get_attributes(self) -> Dict[str, Any]:
        return {
            "user_uuid": self.user_uuid,
            "user_id": self.user_id,
            "nickname": self.nickname,
            "email": self.email,
            "created_at": self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
        }


class CreateUserModel(BaseModel):
    user_id: str
    password: str
    nickname: str
    email: str


class ForgotPasswordModel(BaseModel):
    user_id: str
    password: str


class SignoutModel(ForgotPasswordModel):
    access_token: str


class TokenModel:
    access_token: str

    def __init__(self, user_uuid: str):
        acem = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        sk = os.getenv("SECRET_KEY")
        al = os.getenv("ALGORITHM")

        if acem and sk and al:
            self.access_token = jwt.encode(
                {
                    "sub": user_uuid,
                    "exp": datetime.now() + timedelta(minutes=float(acem)),
                },
                sk,
                algorithm=al,
            )
        else:
            raise FileNotFoundError(
                ".env파일에서 ACCESS_TOKEN_EXPIRE_MINUTES과 SECRET_KEY 환경 변수를 찾을 수 없습니다!"
            )

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
