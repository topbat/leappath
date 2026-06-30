"""求职准备模块模型，前缀 prp_。"""
from typing import Optional

from sqlalchemy import JSON, Boolean, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class PrpQuestionBank(UUIDPk, Timestamped, Base):
    __tablename__ = "prp_question_bank"

    category: Mapped[str] = mapped_column(String(30), index=True)  # common/technical/aptitude/personality
    sub_category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    difficulty: Mapped[str] = mapped_column(String(10), default="medium", index=True)
    question: Mapped[str] = mapped_column(Text)
    answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    answer_tips: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    tags: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    use_count: Mapped[int] = mapped_column(Integer, default=0)


class PrpPracticeRecord(UUIDPk, Timestamped, Base):
    __tablename__ = "prp_practice_record"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    question_id: Mapped[Optional[str]] = mapped_column(
        String(32), ForeignKey("prp_question_bank.id"), nullable=True
    )
    question_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    user_answer: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_feedback: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    score: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    time_spent_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


class PrpOffer(UUIDPk, Timestamped, Base):
    __tablename__ = "prp_offer"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    company_name: Mapped[str] = mapped_column(String(200))
    position_title: Mapped[str] = mapped_column(String(200))
    base_salary: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bonus_months: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    stock_value: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    other_benefits: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    total_annual: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    work_city: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    commute_time: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    evaluation: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    is_accepted: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
