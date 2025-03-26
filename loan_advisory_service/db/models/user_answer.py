from sqlalchemy import ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base
from loan_advisory_service.db.models.admin.question import QuestionCategoryEnum
from loan_advisory_service.db.models.request import RequestStatus


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    request_id: Mapped[int] = mapped_column(ForeignKey("requests.id", ondelete="CASCADE"))
    question_text: Mapped[str] = mapped_column(String, nullable=False)
    group_text: Mapped[str] = mapped_column(String, nullable=True)
    question_category: Mapped[QuestionCategoryEnum] = mapped_column(String, nullable=False,
                                                                    default=QuestionCategoryEnum.main)
    answer_text: Mapped[str | None] = mapped_column(String, nullable=True)
    file_url: Mapped[str | None] = mapped_column(String, nullable=True)
    status_file_added: Mapped[RequestStatus | None] = mapped_column(String, nullable=True,default=RequestStatus.pre_loi.value)
    file_name: Mapped[str | None] = mapped_column(String, nullable=True)
    file_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="answers")
    request: Mapped["Request"] = relationship("Request", back_populates="answers")

