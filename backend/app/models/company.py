"""公司画像模块模型，前缀 cmp_。"""
from datetime import date
from typing import Optional

from sqlalchemy import JSON, Date, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class CmpCompany(UUIDPk, Timestamped, Base):
    __tablename__ = "cmp_company"

    name: Mapped[str] = mapped_column(String(200), index=True)
    short_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)
    size_range: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    financing_stage: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    location_city: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)
    location_address: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    lng: Mapped[Optional[float]] = mapped_column(nullable=True)  # 经度
    lat: Mapped[Optional[float]] = mapped_column(nullable=True)  # 纬度
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    tech_stack: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    culture_tags: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    difficulty_level: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # low/medium/high/extreme
    data_source: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)


class CmpSalary(UUIDPk, Timestamped, Base):
    __tablename__ = "cmp_salary"

    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("cmp_company.id"), index=True)
    position_name: Mapped[str] = mapped_column(String(100))
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_avg: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    bonus_months: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    stock_option: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sample_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    data_year: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    data_source: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)


class CmpReview(UUIDPk, Timestamped, Base):
    __tablename__ = "cmp_review"

    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("cmp_company.id"), index=True)
    review_type: Mapped[str] = mapped_column(String(20), index=True)  # interview/employee
    position_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    interview_round: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    interview_difficulty: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    interview_questions: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    review_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    offer_result: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    publish_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    data_source: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


class CmpUserSaved(UUIDPk, Timestamped, Base):
    __tablename__ = "cmp_user_saved"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    company_id: Mapped[str] = mapped_column(String(32), ForeignKey("cmp_company.id"), index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
