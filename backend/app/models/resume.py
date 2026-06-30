"""简历模块模型，前缀 rsm_。"""
from typing import Optional

from sqlalchemy import JSON, Boolean, ForeignKey, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class RsmResume(UUIDPk, Timestamped, Base):
    __tablename__ = "rsm_resume"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    title: Mapped[str] = mapped_column(String(100), default="我的简历")
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    template_id: Mapped[Optional[str]] = mapped_column(String(50), default="general-classic")
    status: Mapped[str] = mapped_column(String(20), default="draft")  # draft/complete/archived
    score_total: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    score_breakdown: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    source_file_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    parsed_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class RsmSection(UUIDPk, Timestamped, Base):
    __tablename__ = "rsm_section"

    resume_id: Mapped[str] = mapped_column(String(32), ForeignKey("rsm_resume.id"), index=True)
    # personal_info/education/experience/project/skill/certificate/language/self_evaluation
    section_type: Mapped[str] = mapped_column(String(30), index=True)
    sort_order: Mapped[int] = mapped_column(SmallInteger, default=0)
    content: Mapped[dict] = mapped_column(JSON, default=dict)
    ai_suggestions: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)


class RsmVersion(UUIDPk, Timestamped, Base):
    __tablename__ = "rsm_version"

    resume_id: Mapped[str] = mapped_column(String(32), ForeignKey("rsm_resume.id"), index=True)
    version_name: Mapped[str] = mapped_column(String(100))
    target_company: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_position: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_jd_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    snapshot_data: Mapped[dict] = mapped_column(JSON, default=dict)
    match_score: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
