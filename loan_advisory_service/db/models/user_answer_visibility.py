from sqlalchemy import ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base


class AnswerVisibility(Base):
    __tablename__ = "answer_visibility"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id", ondelete="CASCADE"))
    who_can_view: Mapped[int] = mapped_column(ForeignKey('users.id'), ondelete="CASCADE")

