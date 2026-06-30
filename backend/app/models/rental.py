"""租房选址模块模型，前缀 rnt_。"""
from datetime import date, datetime
from typing import Optional

from sqlalchemy import JSON, Boolean, Date, DateTime, Float, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base, Timestamped, UUIDPk


class RntListing(UUIDPk, Timestamped, Base):
    __tablename__ = "rnt_listing"

    title: Mapped[str] = mapped_column(String(300))
    city: Mapped[str] = mapped_column(String(50), index=True)
    district: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    community_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    lng: Mapped[float] = mapped_column(Float, default=0.0)
    lat: Mapped[float] = mapped_column(Float, default=0.0)
    price_monthly: Mapped[int] = mapped_column(Integer, index=True)
    price_deposit: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    room_type: Mapped[Optional[str]] = mapped_column(String(20), index=True)  # studio/1room/2room/3room/4room+
    rent_type: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # whole/share
    area_sqm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    floor_level: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    total_floors: Mapped[Optional[int]] = mapped_column(SmallInteger, nullable=True)
    orientation: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    decoration: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    has_elevator: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    has_balcony: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    has_private_bath: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    images: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    facilities: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    nearby_poi: Mapped[Optional[list]] = mapped_column(JSON, default=list)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    source_platform: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    source_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    listed_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class RntCommute(UUIDPk, Base):
    __tablename__ = "rnt_commute"

    from_lng: Mapped[float] = mapped_column(Float)
    from_lat: Mapped[float] = mapped_column(Float)
    to_lng: Mapped[float] = mapped_column(Float)
    to_lat: Mapped[float] = mapped_column(Float)
    transport_mode: Mapped[str] = mapped_column(String(10))  # walk/subway/drive
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    distance_meters: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    route_detail: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    cached_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
