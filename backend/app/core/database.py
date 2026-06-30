"""数据库引擎、会话与声明式基类。"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def gen_uuid() -> str:
    return uuid.uuid4().hex


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """声明式基类。"""


class UUIDPk:
    """统一的 UUID 主键（SQLite 下用 36 位 hex 字符串）。"""

    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=gen_uuid)


class Timestamped:
    """创建/更新时间戳混入。"""

    created_at: Mapped[datetime] = mapped_column(DateTime, default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=now_utc, onupdate=now_utc
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """创建所有表（导入 models 以注册映射）。"""
    from app import models  # noqa: F401  确保所有模型被导入

    Base.metadata.create_all(bind=engine)
