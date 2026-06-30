"""职位匹配与投递追踪。"""
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db, now_utc
from app.core.deps import get_current_user
from app.core.serialize import model_to_dict, models_to_list
from app.models.company import CmpCompany
from app.models.job import JobApplication, JobPosition
from app.models.resume import RsmResume, RsmSection
from app.models.user import UsrUser
from app.services import ai

router = APIRouter(prefix="/api/jobs", tags=["职位匹配"])

APPLICATION_STAGES = ["saved", "applied", "screening", "interview", "offer", "accepted", "rejected"]
STAGE_LABELS = {
    "saved": "待投递", "applied": "已投递", "screening": "初筛中",
    "interview": "面试中", "offer": "已 Offer", "accepted": "已接受", "rejected": "已拒绝",
}


# ---------- 职位 ----------

@router.get("/positions")
def list_positions(
    city: str | None = None,
    keyword: str | None = None,
    user: UsrUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(JobPosition).filter(JobPosition.is_active == True)  # noqa: E712
    if city:
        q = q.filter(JobPosition.location_city == city)
    if keyword:
        q = q.filter(JobPosition.title.like(f"%{keyword}%"))
    items = q.order_by(JobPosition.created_at.desc()).limit(50).all()
    out = []
    for p in items:
        d = model_to_dict(p)
        if p.company_id:
            c = db.get(CmpCompany, p.company_id)
            d["company"] = {"name": c.name, "logo_url": c.logo_url, "short_name": c.short_name} if c else None
        out.append(d)
    return out


@router.get("/positions/{pid}")
def get_position(pid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.get(JobPosition, pid)
    if not p:
        raise HTTPException(404, "职位不存在")
    d = model_to_dict(p)
    if p.company_id:
        c = db.get(CmpCompany, p.company_id)
        d["company"] = model_to_dict(c) if c else None
    return d


@router.get("/recommended")
def recommended(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """每日推荐：对在招职位计算匹配度后排序取 Top。"""
    resume = db.query(RsmResume).filter(RsmResume.user_id == user.id, RsmResume.is_default == True).first()  # noqa: E712
    if not resume:
        resume = db.query(RsmResume).filter(RsmResume.user_id == user.id).first()
    resume_text = (resume.title if resume else "") + " " + " ".join(user.target_positions or [])
    if resume:
        secs = db.query(RsmSection).filter(RsmSection.resume_id == resume.id).all()
        resume_text += " " + " ".join(str(s.content) for s in secs)
    positions = db.query(JobPosition).filter(JobPosition.is_active == True).limit(30).all()  # noqa: E712
    scored = []
    for p in positions:
        m = ai.match_jd(resume_text, (p.job_description or "") + " " + (p.job_requirements or ""))
        d = model_to_dict(p)
        d["match"] = m["overall"]
        d["match_level"] = m["level"]
        if p.company_id:
            c = db.get(CmpCompany, p.company_id)
            d["company"] = {"name": c.name, "logo_url": c.logo_url} if c else None
        scored.append(d)
    scored.sort(key=lambda x: x["match"], reverse=True)
    return scored[:10]


class MatchIn(BaseModel):
    jd_text: str
    resume_id: str | None = None


@router.post("/match")
def match(body: MatchIn, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    resume = db.get(RsmResume, body.resume_id) if body.resume_id else None
    if not resume:
        resume = db.query(RsmResume).filter(RsmResume.user_id == user.id).first()
    resume_text = (resume.title if resume else "")
    if resume:
        secs = db.query(RsmSection).filter(RsmSection.resume_id == resume.id).all()
        resume_text += " " + " ".join(str(s.content) for s in secs)
    return ai.match_jd(resume_text, body.jd_text)


# ---------- 投递追踪 ----------

@router.get("/applications")
def list_applications(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(JobApplication).filter(JobApplication.user_id == user.id).order_by(JobApplication.updated_at.desc()).all()
    board = {stage: [] for stage in APPLICATION_STAGES}
    for a in items:
        board.setdefault(a.status, []).append(model_to_dict(a))
    return {
        "stages": [{"key": s, "label": STAGE_LABELS[s], "items": board.get(s, [])} for s in APPLICATION_STAGES],
    }


@router.post("/applications")
def create_application(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    a = JobApplication(
        user_id=user.id,
        position_id=body.get("position_id"),
        resume_version_id=body.get("resume_version_id"),
        company_name=body.get("company_name", "未命名公司"),
        position_title=body.get("position_title", "未命名职位"),
        status=body.get("status", "saved"),
        salary_label=body.get("salary_label"),
        notes=body.get("notes"),
        applied_date=date.fromisoformat(body["applied_date"]) if body.get("applied_date") else None,
        status_history=[{"status": body.get("status", "saved"), "at": now_utc().isoformat()}],
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return model_to_dict(a)


@router.put("/applications/{aid}")
def update_application(aid: str, body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    a = db.get(JobApplication, aid)
    if not a or a.user_id != user.id:
        raise HTTPException(404, "投递记录不存在")
    if "status" in body and body["status"] != a.status:
        hist = list(a.status_history or [])
        hist.append({"status": body["status"], "at": now_utc().isoformat()})
        a.status_history = hist
        if body["status"] == "applied" and not a.applied_date:
            a.applied_date = date.today()
    for k in ("company_name", "position_title", "status", "salary_label", "notes", "next_follow_up", "interviews"):
        if k in body:
            if k == "next_follow_up" and body[k]:
                a.next_follow_up = date.fromisoformat(body[k])
            else:
                setattr(a, k, body[k])
    db.commit()
    db.refresh(a)
    return model_to_dict(a)


@router.delete("/applications/{aid}")
def delete_application(aid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    a = db.get(JobApplication, aid)
    if not a or a.user_id != user.id:
        raise HTTPException(404, "投递记录不存在")
    db.delete(a)
    db.commit()
    return {"ok": True}
