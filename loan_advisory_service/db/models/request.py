from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base
from sqlalchemy import Enum

class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default="new")

    user: Mapped["User"] = relationship("User", back_populates="request")
    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="request", cascade="all, delete", passive_deletes=True)

