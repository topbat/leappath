"""公司画像：档案、薪资、面经、收藏与对比。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.serialize import model_to_dict, models_to_list
from app.models.company import CmpCompany, CmpReview, CmpSalary, CmpUserSaved
from app.models.job import JobPosition
from app.models.user import UsrUser

router = APIRouter(prefix="/api/companies", tags=["公司画像"])


@router.get("")
def list_companies(
    keyword: str | None = None,
    industry: str | None = None,
    user: UsrUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(CmpCompany)
    if keyword:
        q = q.filter(CmpCompany.name.like(f"%{keyword}%"))
    if industry:
        q = q.filter(CmpCompany.industry == industry)
    items = q.limit(50).all()
    saved_ids = {s.company_id for s in db.query(CmpUserSaved).filter(CmpUserSaved.user_id == user.id).all()}
    out = []
    for c in items:
        d = model_to_dict(c)
        d["is_saved"] = c.id in saved_ids
        out.append(d)
    return out


@router.get("/saved")
def list_saved(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    saved = db.query(CmpUserSaved).filter(CmpUserSaved.user_id == user.id).all()
    out = []
    for s in saved:
        c = db.get(CmpCompany, s.company_id)
        if c:
            d = model_to_dict(c)
            d["is_saved"] = True
            d["notes"] = s.notes
            out.append(d)
    return out


@router.get("/{cid}")
def get_company(cid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    c = db.get(CmpCompany, cid)
    if not c:
        raise HTTPException(404, "公司不存在")
    salaries = db.query(CmpSalary).filter(CmpSalary.company_id == cid).all()
    reviews = db.query(CmpReview).filter(CmpReview.company_id == cid).all()
    positions = db.query(JobPosition).filter(JobPosition.company_id == cid, JobPosition.is_active == True).all()  # noqa: E712
    saved = db.query(CmpUserSaved).filter(CmpUserSaved.user_id == user.id, CmpUserSaved.company_id == cid).first()
    d = model_to_dict(c)
    d["salaries"] = models_to_list(salaries)
    d["reviews"] = models_to_list(reviews)
    d["positions"] = models_to_list(positions)
    d["is_saved"] = saved is not None
    # 面经 AI 摘要（基于已有面经的高频问题聚合）
    questions = []
    for r in reviews:
        questions.extend(r.interview_questions or [])
    d["review_summary"] = {
        "count": len(reviews),
        "hot_questions": list(dict.fromkeys(questions))[:5],
    }
    return d


@router.post("/{cid}/save")
def toggle_save(cid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    c = db.get(CmpCompany, cid)
    if not c:
        raise HTTPException(404, "公司不存在")
    existing = db.query(CmpUserSaved).filter(CmpUserSaved.user_id == user.id, CmpUserSaved.company_id == cid).first()
    if existing:
        db.delete(existing)
        db.commit()
        return {"is_saved": False}
    db.add(CmpUserSaved(user_id=user.id, company_id=cid))
    db.commit()
    return {"is_saved": True}


@router.post("/compare")
def compare(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    ids = body.get("company_ids", [])
    out = []
    for cid in ids:
        c = db.get(CmpCompany, cid)
        if not c:
            continue
        salaries = db.query(CmpSalary).filter(CmpSalary.company_id == cid).all()
        avg = round(sum(s.salary_avg or 0 for s in salaries) / len(salaries)) if salaries else None
        out.append({
            "id": c.id, "name": c.name, "industry": c.industry, "size_range": c.size_range,
            "financing_stage": c.financing_stage, "location_city": c.location_city,
            "difficulty_level": c.difficulty_level, "culture_tags": c.culture_tags,
            "avg_salary": avg,
        })
    return out
