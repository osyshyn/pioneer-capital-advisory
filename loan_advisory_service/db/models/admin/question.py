from sqlalchemy import String, ForeignKey, Integer, Index
from enum import Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base


class QuestionTypeEnum(str, Enum):
    text = "text"
    number = "number"
    choice = "choice"
    file = "file"
    email = "email"
    phone_number = "phone_number"


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    sub_text: Mapped[str] = mapped_column(String, nullable=True)
    type: Mapped[QuestionTypeEnum] = mapped_column(nullable=False)
    is_required: Mapped[bool] = mapped_column(default=True)

    order: Mapped[int] = mapped_column(Integer, nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("question_groups.id", ondelete="CASCADE"))

    group: Mapped["QuestionGroup"] = relationship(back_populates="questions")
    options: Mapped[list["AnswerOption"]] = relationship(back_populates="question", cascade="all, delete",
                                                         passive_deletes=True)

    __table_args__ = (
        Index('ix_question_order_group', 'order', 'group_id', unique=True),
    )
