"""求职规划模块模型，前缀 pln_。"""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import JSON, Boolean, Date, DateTime, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class PlnPlan(UUIDPk, Timestamped, Base):
    __tablename__ = "pln_plan"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), unique=True, index=True)
    target_industry: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_position: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    target_start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    timeline: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    current_progress: Mapped[int] = mapped_column(SmallInteger, default=0)


class PlnSkillAssessment(UUIDPk, Timestamped, Base):
    __tablename__ = "pln_skill_assessment"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    assessment_type: Mapped[str] = mapped_column(String(20), default="self")  # self/ai
    skills: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    radar_chart_data: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    gap_analysis: Mapped[Optional[list]] = mapped_column(JSON, default=list)


class PlnLearningPath(UUIDPk, Timestamped, Base):
    __tablename__ = "pln_learning_path"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    skill_name: Mapped[str] = mapped_column(String(100))
    resources: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    estimated_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    completed_hours: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(20), default="in_progress")


class PlnDailyTask(UUIDPk, Timestamped, Base):
    __tablename__ = "pln_daily_task"

    user_id: Mapped[str] = mapped_column(String(32), ForeignKey("usr_user.id"), index=True)
    task_date: Mapped[date] = mapped_column(Date, index=True)
    task_type: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)  # apply/study/practice/interview/other
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    sort_order: Mapped[int] = mapped_column(SmallInteger, default=0)
