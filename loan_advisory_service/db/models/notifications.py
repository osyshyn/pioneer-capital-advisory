from sqlalchemy import ForeignKey, Integer, String,Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base
from sqlalchemy import Enum

class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    message: Mapped[str] = mapped_column(String, nullable=False)

    users: Mapped[list["User"]] = relationship(
        secondary="notification_users", back_populates="notifications"
    )

class NotificationUser(Base):
    __tablename__ = "notification_users"

    notification_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("notifications.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
