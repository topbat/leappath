"""租房选址：房源、地图找房、通勤估算、预算计算、城市对比。"""
import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.serialize import model_to_dict
from app.models.company import CmpCompany
from app.models.rental import RntListing
from app.models.user import UsrUser

router = APIRouter(prefix="/api/rental", tags=["租房选址"])

# 各交通方式估算速度（米/分钟）
_SPEED = {"walk": 80, "subway": 500, "drive": 600}


def _haversine(lng1, lat1, lng2, lat2) -> float:
    r = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lng2 - lng1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def _commute_minutes(dist_m: float, mode: str) -> int:
    return max(1, round(dist_m / _SPEED.get(mode, 500)))


@router.get("/listings")
def list_listings(
    city: str | None = None,
    price_min: int | None = None,
    price_max: int | None = None,
    room_type: str | None = None,
    rent_type: str | None = None,
    near_subway: bool | None = None,
    center_lng: float | None = Query(default=None),
    center_lat: float | None = Query(default=None),
    mode: str = "subway",
    db: Session = Depends(get_db),
    user: UsrUser = Depends(get_current_user),
):
    q = db.query(RntListing).filter(RntListing.is_active == True)  # noqa: E712
    if city:
        q = q.filter(RntListing.city == city)
    if price_min is not None:
        q = q.filter(RntListing.price_monthly >= price_min)
    if price_max is not None:
        q = q.filter(RntListing.price_monthly <= price_max)
    if room_type:
        q = q.filter(RntListing.room_type == room_type)
    if rent_type:
        q = q.filter(RntListing.rent_type == rent_type)
    items = q.limit(200).all()
    out = []
    for r in items:
        d = model_to_dict(r)
        if center_lng is not None and center_lat is not None:
            dist = _haversine(center_lng, center_lat, r.lng, r.lat)
            d["distance_m"] = round(dist)
            d["commute_minutes"] = _commute_minutes(dist, mode)
        out.append(d)
    if center_lng is not None and center_lat is not None:
        out.sort(key=lambda x: x.get("commute_minutes", 9999))
    return out


@router.get("/listings/{lid}")
def get_listing(lid: str, db: Session = Depends(get_db), user: UsrUser = Depends(get_current_user)):
    r = db.get(RntListing, lid)
    if not r:
        raise HTTPException(404, "房源不存在")
    return model_to_dict(r)


@router.get("/company-centers")
def company_centers(db: Session = Depends(get_db), user: UsrUser = Depends(get_current_user)):
    """提供可作为地图中心的公司地点（有坐标的公司）。"""
    items = db.query(CmpCompany).filter(CmpCompany.lat.isnot(None)).all()
    return [
        {"id": c.id, "name": c.name, "address": c.location_address, "city": c.location_city,
         "lng": c.lng, "lat": c.lat}
        for c in items if c.lng and c.lat
    ]


@router.post("/commute-circles")
def commute_circles(body: dict, db: Session = Depends(get_db), user: UsrUser = Depends(get_current_user)):
    """以公司为中心，统计各时间圈内房源数量。"""
    lng, lat = body["center_lng"], body["center_lat"]
    mode = body.get("mode", "subway")
    rings = body.get("rings", [15, 30, 45, 60])
    city = body.get("city")
    q = db.query(RntListing).filter(RntListing.is_active == True)  # noqa: E712
    if city:
        q = q.filter(RntListing.city == city)
    listings = q.all()
    buckets = {r: 0 for r in rings}
    for li in listings:
        mins = _commute_minutes(_haversine(lng, lat, li.lng, li.lat), mode)
        for r in rings:
            if mins <= r:
                buckets[r] += 1
                break
    speed = _SPEED.get(mode, 500)
    return {
        "mode": mode,
        "circles": [
            {"minutes": r, "radius_m": round(speed * r), "count": buckets[r]}
            for r in rings
        ],
    }


@router.post("/budget")
def budget(body: dict, user: UsrUser = Depends(get_current_user)):
    """预算计算器：税前月薪 -> 税后估算 + 建议租金上限。"""
    gross = body.get("gross_monthly", 0) or 0
    # 简化版税后估算（社保公积金约 18% + 个税近似）
    after_tax = round(gross * 0.78)
    rent_cap = round(after_tax * 0.30)
    return {
        "gross_monthly": gross,
        "after_tax": after_tax,
        "rent_ratio": 0.30,
        "recommended_rent_cap": rent_cap,
        "other_expenses": {
            "utilities": round(after_tax * 0.05),
            "commute": round(after_tax * 0.06),
            "food": round(after_tax * 0.20),
        },
        "estimated_savings": round(after_tax - rent_cap - after_tax * 0.31),
    }


@router.get("/city-compare")
def city_compare(db: Session = Depends(get_db), user: UsrUser = Depends(get_current_user)):
    """城市横向对比：薪资购买力 / 租金指数 / 生活成本 / 净结余。"""
    cities = {}
    for r in db.query(RntListing).all():
        cities.setdefault(r.city, []).append(r.price_monthly)
    presets = {
        "北京": {"salary": 30000, "cost": 4500},
        "上海": {"salary": 29000, "cost": 4400},
        "深圳": {"salary": 28000, "cost": 4200},
        "杭州": {"salary": 25000, "cost": 3600},
        "广州": {"salary": 24000, "cost": 3500},
        "成都": {"salary": 19000, "cost": 2800},
    }
    out = []
    for city, prices in cities.items():
        avg_rent = round(sum(prices) / len(prices)) if prices else 0
        preset = presets.get(city, {"salary": 20000, "cost": 3000})
        net = preset["salary"] - avg_rent - preset["cost"]
        out.append({
            "city": city, "avg_salary": preset["salary"], "avg_rent": avg_rent,
            "living_cost": preset["cost"], "net_savings": net,
            "listing_count": len(prices),
        })
    out.sort(key=lambda x: x["net_savings"], reverse=True)
    return out
