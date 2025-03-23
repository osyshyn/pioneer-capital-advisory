from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from loan_advisory_service.db.models.base import Base
import enum


class RequestStatus(str, enum.Enum):
    pre_loi = "Pre-LOI"
    loi = "LOI"
    scheduled_call = "Scheduled Call"
    signed_engagement = "Signed Engagement Letter"
    document_submission = "Document Submission"
    credit_profile = "Credit Profile Preparation"
    credit_approval = "Credit Approval"
    signed_term_sheet = "Signed Term Sheet"
    closure = "Closure"
    funded = "Funded"


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String, nullable=False, default=RequestStatus.pre_loi.value)

    users: Mapped[list["User"]] = relationship(
        "User", secondary="user_requests", back_populates="request"
    )
    answers: Mapped[list["Answer"]] = relationship("Answer", back_populates="request", cascade="all, delete",
                                                   passive_deletes=True)
