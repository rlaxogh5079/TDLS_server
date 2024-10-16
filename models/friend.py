from sqlalchemy import String, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any
from models.base import Base
from enum import Enum
import uuid


class FriendStatus(Enum):
    pending = 0  # 대기 중
    accepted = 1  # 수락 됨
    rejected = 2  # 거절 됨
    block = 3  # 차단 됨


class Friend(Base):
    __tablename__ = "Friend"

    transmit_user_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    receive_user_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    status: Mapped[FriendStatus] = mapped_column(
        SQLEnum(FriendStatus), default=FriendStatus.pending
    )
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_uuid1"],
            ["User.user_uuid"],
        ),
        ForeignKeyConstraint(
            ["user_uuid2"],
            ["User.user_uuid"],
        ),
    )

    def get_attributes(self) -> Dict[str, Any]:
        return {
            "user_uuid1": self.user_uuid1,
            "user_uuid2": self.user_uuid2,
            "status": Friend.convert_status_korean(self.status),
            "created_at": self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
        }

    @staticmethod
    def convert_status_korean(status: FriendStatus):
        return {
            FriendStatus.pending: "대기 중",
            FriendStatus.accepted: "수락 됨",
            FriendStatus.rejected: "거절 됨",
            FriendStatus.block: "차단 됨",
        }[status]
