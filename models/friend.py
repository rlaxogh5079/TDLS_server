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
    canceled = 4  # 취소 됨


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
            ["transmit_user_uuid"],
            ["User.user_uuid"],
        ),
        ForeignKeyConstraint(
            ["receive_user_uuid"],
            ["User.user_uuid"],
        ),
    )

    def __init__(
        self,
        transmit_user_uuid: str,
        receive_user_uuid: str,
        status: FriendStatus | None = None,
        created_at: datetime | None = None,
    ):
        self.transmit_user_uuid = transmit_user_uuid
        self.receive_user_uuid = receive_user_uuid
        self.status = status if status else FriendStatus.pending
        self.created_at = created_at if created_at else datetime.now()

    def get_attributes(self) -> Dict[str, Any]:
        return {
            "transmit_user_uuid": self.transmit_user_uuid,
            "receive_user_uuid": self.receive_user_uuid,
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
