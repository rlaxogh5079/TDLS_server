from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, TEXT
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any
from models.base import Base
from enum import Enum
import uuid


class User(Base):
    __tablename__ = "User"

    user_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    nickname: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())
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
        self.user_uuid = user_uuid if user_uuid else str(uuid.uuid4())
        self.user_id = user_id
        self.password = password
        self.nickname = nickname
        self.email = email
        self.created_at = created_at if created_at else datetime.now()
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


class ExistErrorCode(Enum):
    USEFUL = 1  # 사용가능
    USERID = 2  # 아이디가 중복됨
    NICKNAME = 3  # 닉네임이 중복됨
    EMAIL = 4  # 이메일이 중복됨


class VerifyErrorCode(Enum):
    SUCCESS = 1  # 인증 성공
    WRONG_VERIFY_CODE = 2  # 인증 코드가 잘못됨
    TIMEOUT = 3  # 타임 아웃
