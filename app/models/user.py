from __future__ import annotations

from typing import TYPE_CHECKING
from sqlalchemy import String, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base
from app.utils.custom_types import uuid_pk, UserType, created_at as created_at_sql
from app.models.roles import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid_pk]
    phone: Mapped[str] = mapped_column(String(50), unique=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True, unique=True)
    full_name: Mapped[str] = mapped_column(String(50))
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), default=UserType.individual)
    created_at: Mapped[created_at_sql]
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    user_roles: Mapped[list[UserRole]] = relationship(
        "UserRole",
        back_populates="user",
        cascade="all, delete-orphan",
    )
