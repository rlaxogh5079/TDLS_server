from sqlalchemy import String, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Dict, Any
from model.base import Base
from enum import Enum
import uuid


class Room(Base):
    __tablename__ = "Room"

    room_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    room_name: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now())

    def __init__(self, room_name: str, created_at: datetime | None = None):
        self.room_name = room_name
        self.created_at = created_at if created_at else datetime.now()

    def get_attributes(self) -> Dict[str, Any]:
        return {
            "room_uuid": self.room_uuid,
            "room_name": self.room_name,
            "created_at": self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
        }


class RoomEntryStatus(Enum):
    pending = 0  # 대기 중
    accepted = 1  # 수락 됨
    rejected = 2  # 거절 됨
    canceled = 4  # 취소 됨


class RoomEntry(Base):
    __tablename__ = "RoomEntry"

    room_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now())
    status: Mapped[RoomEntryStatus] = mapped_column(
        SQLEnum(RoomEntryStatus), default=RoomEntryStatus.pending
    )
