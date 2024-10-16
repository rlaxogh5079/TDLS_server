from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import String
from typing import Dict, Any
from models.base import Base
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
