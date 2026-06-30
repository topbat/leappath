"""职位与投递模块模型，前缀 job_。"""
from datetime import date
from typing import Optional

from sqlalchemy import JSON, Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class JobPosition(UUIDPk, Timestamped, Base):
    __tablename__ = "job_position"

    company_id: Mapped[Optional[str]] = mapped_column(
        String(32), ForeignKey("cmp_company.id"), index=True, nullable=True
    )
    title: Mapped[str] = mapped_column(String(200), index=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    location_city: Mapped[Optional[str]] = mapped_column(String(50), index=True, nullable=True)
    location_district: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    salary_period: Mapped[Optional[str]] = mapped_column(String(10), default="month")
    experience_required: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    education_required: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    job_description: Mapped[str] = mapped_column(Text, default="")
    job_requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    job_tags: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    job_type: Mapped[Optional[str]] = mapped_column(String(20), default="fulltime")
    source_platform: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    source_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    posted_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    expire_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)


class JobApplication(UUIDPk, Timestamped, Base):
    __tablename__ = "job_application"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    position_id: Mapped[Optional[str]] = mapped_column(
        String(32), ForeignKey("job_position.id"), nullable=True
    )
    resume_version_id: Mapped[Optional[str]] = mapped_column(
        String(32), ForeignKey("rsm_version.id"), nullable=True
    )
    company_name: Mapped[str] = mapped_column(String(200))
    position_title: Mapped[str] = mapped_column(String(200))
    # saved/applied/screening/interview/offer/accepted/rejected
    status: Mapped[str] = mapped_column(String(20), default="saved", index=True)
    salary_label: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    applied_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_follow_up: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    interviews: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    status_history: Mapped[Optional[list]] = mapped_column(JSON, default=list)
