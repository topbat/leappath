"""模拟面试模块模型，前缀 itv_。"""
from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class ItvSession(UUIDPk, Timestamped, Base):
    __tablename__ = "itv_session"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    resume_id: Mapped[Optional[str]] = mapped_column(
        String(32), ForeignKey("rsm_resume.id"), nullable=True
    )
    interview_type: Mapped[str] = mapped_column(String(20))  # technical/behavioral/hr/group/case
    industry: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    position: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(10), default="medium")
    total_questions: Mapped[int] = mapped_column(SmallInteger, default=8)
    status: Mapped[str] = mapped_column(String(20), default="in_progress", index=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class ItvMessage(UUIDPk, Timestamped, Base):
    __tablename__ = "itv_message"

    session_id: Mapped[str] = mapped_column(String(32), ForeignKey("itv_session.id"), index=True)
    role: Mapped[str] = mapped_column(String(10))  # interviewer/user/system
    message_type: Mapped[str] = mapped_column(String(20), default="text")
    content: Mapped[str] = mapped_column(Text)
    question_number: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    feedback: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    token_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class ItvReport(UUIDPk, Timestamped, Base):
    __tablename__ = "itv_report"

    session_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("itv_session.id"), unique=True, index=True
    )
    overall_score: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    score_breakdown: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    strengths: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    weaknesses: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    suggestions: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    question_reviews: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
