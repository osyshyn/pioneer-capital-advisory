from sqlalchemy import String, ForeignKey, Integer
from enum import Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base


class QuestionTypeEnum(str, Enum):
    text = "text"
    number = "number"
    choice = "choice"


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[QuestionTypeEnum] = mapped_column(nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("question_groups.id", ondelete="CASCADE"))

    group: Mapped["QuestionGroup"] = relationship(back_populates="questions")
    options: Mapped[list["AnswerOption"]] = relationship(back_populates="question", cascade="all, delete",
                                                         passive_deletes=True)
