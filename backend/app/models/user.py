"""用户模块模型，前缀 usr_。"""
from typing import Optional

from sqlalchemy import JSON, Boolean, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class UsrUser(UUIDPk, Timestamped, Base):
    __tablename__ = "usr_user"

    wechat_openid: Mapped[Optional[str]] = mapped_column(String(64), unique=True, nullable=True)
    wechat_unionid: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    password_hash: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    nickname: Mapped[str] = mapped_column(String(50), default="求职者")
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    gender: Mapped[int] = mapped_column(SmallInteger, default=0)
    birth_year: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    current_city: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_cities: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    education_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    years_of_experience: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    current_industry: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_industries: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    target_positions: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    expected_salary_min: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    expected_salary_max: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
