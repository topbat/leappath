"""系统辅助模块模型，前缀 sys_。"""
from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class SysUserQuota(UUIDPk, Timestamped, Base):
    __tablename__ = "sys_user_quota"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), unique=True, index=True)
    resume_optimize_count: Mapped[int] = mapped_column(Integer, default=0)
    mock_interview_count: Mapped[int] = mapped_column(Integer, default=0)
    interview_quota_total: Mapped[int] = mapped_column(Integer, default=10)
    interview_quota_used: Mapped[int] = mapped_column(Integer, default=0)
    quota_reset_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)


class SysAiLog(UUIDPk, Timestamped, Base):
    __tablename__ = "sys_ai_log"

    user_id: Mapped[Optional[str]] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True, nullable=True)
    gen_type: Mapped[str] = mapped_column(String(30), index=True)
    prompt_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    duration_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    success: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
