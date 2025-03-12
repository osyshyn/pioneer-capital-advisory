from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loan_advisory_service.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool | None] = mapped_column(default=False)

    is_two_factor_enabled: Mapped[bool | None] = mapped_column(default=False)
    two_factor_secret: Mapped[str | None] = mapped_column(String(225), default=None)

    roles = relationship("Role", secondary="user_roles", back_populates="users")

