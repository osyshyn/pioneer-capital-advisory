from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base

class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id", ondelete="CASCADE"))
    question_text: Mapped[str] = mapped_column(String, nullable=False)
    answer_text: Mapped[str | None] = mapped_column(String, nullable=True)
    answer_option_text: Mapped[str | None] = mapped_column(String, nullable=True)
    file_url: Mapped[str | None] = mapped_column(String, nullable=True)


    user: Mapped["User"] = relationship("User", back_populates="answers")
    request: Mapped["Request"] = relationship("Request", back_populates="answers")