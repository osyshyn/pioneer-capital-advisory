from sqlalchemy import String, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base


class QuestionGroup(Base):
    __tablename__ = "question_groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False)
    order: Mapped[int] = mapped_column(nullable=False, unique=True)

    questions: Mapped[list["Question"]] = relationship(back_populates="group", order_by="Question.order",
                                                       cascade="all, delete",
                                                       passive_deletes=True,
                                                       )
