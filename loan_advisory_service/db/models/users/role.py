from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loan_advisory_service.db.models.base import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)

    users: Mapped[list['User']] = relationship('User', secondary='user_roles', back_populates='roles')

    permissions: Mapped[list['Permission']] = relationship('Permission', secondary='role_permissions',
                                                           back_populates='roles')
