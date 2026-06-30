"""简历中心：CRUD、分块、润色、评分、定向优化、版本管理。"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.serialize import model_to_dict, models_to_list
from app.models.resume import RsmResume, RsmSection, RsmVersion
from app.models.user import UsrUser
from app.services import ai

router = APIRouter(prefix="/api/resumes", tags=["简历中心"])


def _sections_text(db: Session, resume_id: str) -> str:
    secs = db.query(RsmSection).filter(RsmSection.resume_id == resume_id).all()
    parts = []
    for s in secs:
        parts.append(str(s.content))
    return " ".join(parts)


@router.get("")
def list_resumes(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(RsmResume).filter(RsmResume.user_id == user.id).order_by(RsmResume.updated_at.desc()).all()
    return models_to_list(items)


@router.post("")
def create_resume(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    r = RsmResume(
        user_id=user.id,
        title=body.get("title", "我的简历"),
        template_id=body.get("template_id", "general-classic"),
        is_default=body.get("is_default", False),
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return model_to_dict(r)


@router.get("/{resume_id}")
def get_resume(resume_id: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.get(RsmResume, resume_id)
    if not r or r.user_id != user.id:
        raise HTTPException(404, "简历不存在")
    secs = db.query(RsmSection).filter(RsmSection.resume_id == resume_id).order_by(RsmSection.sort_order).all()
    versions = db.query(RsmVersion).filter(RsmVersion.resume_id == resume_id).all()
    data = model_to_dict(r)
    data["sections"] = models_to_list(secs)
    data["versions"] = models_to_list(versions)
    return data


@router.put("/{resume_id}")
def update_resume(resume_id: str, body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.get(RsmResume, resume_id)
    if not r or r.user_id != user.id:
        raise HTTPException(404, "简历不存在")
    for k in ("title", "template_id", "is_default", "status"):
        if k in body:
            setattr(r, k, body[k])
    db.commit()
    db.refresh(r)
    return model_to_dict(r)


@router.delete("/{resume_id}")
def delete_resume(resume_id: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.get(RsmResume, resume_id)
    if not r or r.user_id != user.id:
        raise HTTPException(404, "简历不存在")
    db.query(RsmSection).filter(RsmSection.resume_id == resume_id).delete()
    db.query(RsmVersion).filter(RsmVersion.resume_id == resume_id).delete()
    db.delete(r)
    db.commit()
    return {"ok": True}


# ---------- 分块 ----------

@router.put("/{resume_id}/sections")
def upsert_sections(resume_id: str, body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """整体覆盖式保存分块：body = {sections: [{section_type, sort_order, content}]}"""
    r = db.get(RsmResume, resume_id)
    if not r or r.user_id != user.id:
        raise HTTPException(404, "简历不存在")
    db.query(RsmSection).filter(RsmSection.resume_id == resume_id).delete()
    for i, sec in enumerate(body.get("sections", [])):
        db.add(RsmSection(
            resume_id=resume_id,
            section_type=sec.get("section_type", "experience"),
            sort_order=sec.get("sort_order", i),
            content=sec.get("content", {}),
        ))
    r.status = "complete"
    db.commit()
    secs = db.query(RsmSection).filter(RsmSection.resume_id == resume_id).order_by(RsmSection.sort_order).all()
    return models_to_list(secs)


# ---------- AI 润色 ----------

class PolishIn(BaseModel):
    text: str
    style: str = "professional"
    target: str | None = None


@router.post("/{resume_id}/polish")
def polish(resume_id: str, body: PolishIn, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    return ai.polish_resume_item(body.text, body.style, body.target)


# ---------- AI 评分 ----------

@router.post("/{resume_id}/score")
def score(resume_id: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.get(RsmResume, resume_id)
    if not r or r.user_id != user.id:
        raise HTTPException(404, "简历不存在")
    secs = db.query(RsmSection).filter(RsmSection.resume_id == resume_id).all()
    result = ai.score_resume(r.title, models_to_list(secs))
    r.score_total = result["score_total"]
    r.score_breakdown = result
    db.commit()
    return result


# ---------- 定向优化（JD 匹配） ----------

class MatchIn(BaseModel):
    jd_text: str


@router.post("/{resume_id}/match")
def match(resume_id: str, body: MatchIn, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.get(RsmResume, resume_id)
    if not r or r.user_id != user.id:
        raise HTTPException(404, "简历不存在")
    resume_text = r.title + " " + _sections_text(db, resume_id)
    return ai.match_jd(resume_text, body.jd_text)


# ---------- 版本管理 ----------

@router.post("/{resume_id}/versions")
def create_version(resume_id: str, body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    r = db.get(RsmResume, resume_id)
    if not r or r.user_id != user.id:
        raise HTTPException(404, "简历不存在")
    match_score = None
    if body.get("target_jd_text"):
        match_score = ai.match_jd(r.title + " " + _sections_text(db, resume_id), body["target_jd_text"])["overall"]
    v = RsmVersion(
        resume_id=resume_id,
        version_name=body.get("version_name", "新版本"),
        target_company=body.get("target_company"),
        target_position=body.get("target_position"),
        target_jd_text=body.get("target_jd_text"),
        snapshot_data=body.get("snapshot_data", {}),
        match_score=match_score,
    )
    db.add(v)
    db.commit()
    db.refresh(v)
    return model_to_dict(v)


@router.get("/{resume_id}/versions")
def list_versions(resume_id: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(RsmVersion).filter(RsmVersion.resume_id == resume_id).all()
    return models_to_list(items)
