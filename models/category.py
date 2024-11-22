from sqlalchemy import String, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Dict, Any
from models.base import Base
from enum import Enum
import uuid


class Category(Base):
    __tablename__ = "Category"

    category_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    category_name: Mapped[str] = mapped_column(String(30), nullable=False)
    owner_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())
    room_uuid: Mapped[str] = mapped_column(String(36), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["owner_uuid"],
            ["User.user_uuid"],
        ),
        ForeignKeyConstraint(
            ["room_uuid"],
            ["Room.room_uuid"],
        ),
    )

    def __init__(
        self,
        category_name: str,
        owner_uuid: str,
        room_uuid: str,
        created_at: datetime | None = None,
    ):
        self.category_name = category_name
        self.owner_uuid = owner_uuid
        self.room_uuid = room_uuid
        self.created_at = created_at if created_at else datetime.now()

    def get_attributes(self) -> Dict[str, Any]:
        return {
            "category_uuid": self.category_uuid,
            "category_name": self.category_name,
            "owner_uuid": self.owner_uuid,
            "created_at": self.created_at.strftime("%Y/%m/%d %H:%M:%S"),
        }
