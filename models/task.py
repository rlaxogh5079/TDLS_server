from sqlalchemy import String, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Dict, Any
from models.base import Base
from enum import Enum
import uuid


class Task(Base):
    __tablename__ = "Task"

    task_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    category_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    user_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    room_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())
    end_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

    __table_args__ = (
        ForeignKeyConstraint(
            ["category_uuid"],
            ["Category.category_uuid"],
        ),
        ForeignKeyConstraint(
            ["user_uuid"],
            ["User.user_uuid"],
        ),
        ForeignKeyConstraint(
            ["room_uuid"],
            ["Room.room_uuid"],
        ),
    )

    def __init__(
        self,
        title: str,
        content: str,
        category_uuid: str,
        user_uuid: str,
        room_uuid: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        end_at: datetime | None = None,
    ):
        self.title = title
        self.content = content
        self.category_uuid = category_uuid
        self.user_uuid = user_uuid
        self.room_uuid = room_uuid
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self.end_at = end_at if end_at else datetime.now()

    def get_attributes(self) -> Dict[str, Any]:
        return {
            "task_uuid": self.task_uuid,
            "title": self.title,
            "content": self.content,
            "category_uuid": self.category_uuid,
            "user_uuid": self.user_uuid,
            "room_uuid": self.room_uuid,
            "created_at": self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
            "updated_at": self.updated_at.strftime("%Y/%m/%d %H:%M:%S"),
            "end_at": self.end_at.strftime("%Y/%m/%d %H:%M:%S"),
        }
