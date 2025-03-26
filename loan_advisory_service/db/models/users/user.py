from sqlalchemy import String,BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from loan_advisory_service.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool | None] = mapped_column(default=False)

    is_two_factor_enabled: Mapped[bool | None] = mapped_column(default=False)
    two_factor_secret: Mapped[str | None] = mapped_column(String(225), default=None)
    folder_id: Mapped[int | None] = mapped_column(BigInteger, default=None)

    roles = relationship("Role", secondary="user_roles", back_populates="users")
    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="user", cascade="all, delete",
                                                   passive_deletes=True)
    request: Mapped[list["Request"]] = relationship(
        "Request", secondary="user_requests", back_populates="users"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        secondary="notification_users", back_populates="users"
    )
