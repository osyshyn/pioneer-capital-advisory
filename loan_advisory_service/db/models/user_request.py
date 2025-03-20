from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base
from sqlalchemy import Enum

class UserRequest(Base):
    __tablename__ = "user_requests"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    request_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("requests.id", ondelete="CASCADE"), primary_key=True
    )

    user: Mapped["User"] = relationship()
    request: Mapped["Request"] = relationship()