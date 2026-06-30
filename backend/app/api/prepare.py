"""求职准备：题库、练习批改、薪资谈判、Offer 评估。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.serialize import model_to_dict, models_to_list
from app.models.prepare import PrpOffer, PrpPracticeRecord, PrpQuestionBank
from app.models.user import UsrUser
from app.services import ai

router = APIRouter(prefix="/api/prepare", tags=["求职准备"])


@router.get("/questions")
def list_questions(
    category: str | None = None,
    sub_category: str | None = None,
    difficulty: str | None = None,
    db: Session = Depends(get_db),
    user: UsrUser = Depends(get_current_user),
):
    q = db.query(PrpQuestionBank)
    if category:
        q = q.filter(PrpQuestionBank.category == category)
    if sub_category:
        q = q.filter(PrpQuestionBank.sub_category == sub_category)
    if difficulty:
        q = q.filter(PrpQuestionBank.difficulty == difficulty)
    items = q.limit(100).all()
    return models_to_list(items)


@router.get("/questions/categories")
def categories(db: Session = Depends(get_db), user: UsrUser = Depends(get_current_user)):
    rows = db.query(PrpQuestionBank.category, PrpQuestionBank.sub_category).all()
    cats: dict[str, set] = {}
    for cat, sub in rows:
        cats.setdefault(cat, set())
        if sub:
            cats[cat].add(sub)
    return {k: sorted(v) for k, v in cats.items()}


@router.post("/practice")
def submit_practice(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    answer = body.get("user_answer", "")
    fb = ai.interview_feedback(answer, body.get("question_number", 1))
    rec = PrpPracticeRecord(
        user_id=user.id,
        question_id=body.get("question_id"),
        question_text=body.get("question_text"),
        user_answer=answer,
        ai_feedback=fb,
        score=fb.get("quality"),
        time_spent_seconds=body.get("time_spent_seconds"),
    )
    db.add(rec)
    if body.get("question_id"):
        q = db.get(PrpQuestionBank, body["question_id"])
        if q:
            q.use_count += 1
    db.commit()
    db.refresh(rec)
    return model_to_dict(rec)


# ---------- 薪资谈判 ----------

@router.post("/negotiation")
def negotiation(body: dict, user: UsrUser = Depends(get_current_user)):
    return ai.negotiation_advice(body.get("base_offer"), body.get("market_avg"))


# ---------- Offer 评估 ----------

DIM_LABELS = {"salary": "薪资", "growth": "成长空间", "wlb": "WLB", "location": "地点", "stability": "稳定性", "team": "团队"}


@router.get("/offers")
def list_offers(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(PrpOffer).filter(PrpOffer.user_id == user.id).all()
    return models_to_list(items)


@router.post("/offers")
def create_offer(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    base = body.get("base_salary", 0) or 0
    bonus = body.get("bonus_months", 0) or 0
    stock = body.get("stock_value", 0) or 0
    total_annual = base * (12 + bonus) + stock
    o = PrpOffer(
        user_id=user.id,
        company_name=body.get("company_name", "未命名公司"),
        position_title=body.get("position_title", "未命名职位"),
        base_salary=base,
        bonus_months=bonus,
        stock_value=stock,
        other_benefits=body.get("other_benefits"),
        total_annual=total_annual,
        work_city=body.get("work_city"),
        commute_time=body.get("commute_time"),
        evaluation=body.get("evaluation"),
        notes=body.get("notes"),
    )
    db.add(o)
    db.commit()
    db.refresh(o)
    return model_to_dict(o)


@router.put("/offers/{oid}")
def update_offer(oid: str, body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    o = db.get(PrpOffer, oid)
    if not o or o.user_id != user.id:
        raise HTTPException(404, "Offer 不存在")
    for k in ("company_name", "position_title", "base_salary", "bonus_months", "stock_value",
              "other_benefits", "work_city", "commute_time", "evaluation", "is_accepted", "notes"):
        if k in body:
            setattr(o, k, body[k])
    if any(k in body for k in ("base_salary", "bonus_months", "stock_value")):
        o.total_annual = (o.base_salary or 0) * (12 + (o.bonus_months or 0)) + (o.stock_value or 0)
    db.commit()
    db.refresh(o)
    return model_to_dict(o)


@router.delete("/offers/{oid}")
def delete_offer(oid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    o = db.get(PrpOffer, oid)
    if not o or o.user_id != user.id:
        raise HTTPException(404, "Offer 不存在")
    db.delete(o)
    db.commit()
    return {"ok": True}


@router.post("/offers/compare")
def compare_offers(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    """多 Offer 雷达对比 + 综合推荐指数。"""
    ids = body.get("offer_ids")
    q = db.query(PrpOffer).filter(PrpOffer.user_id == user.id)
    if ids:
        q = q.filter(PrpOffer.id.in_(ids))
    offers = q.all()
    dims = ["salary", "growth", "wlb", "location", "stability", "team"]
    result = []
    max_total = max((o.total_annual or 0) for o in offers) or 1
    for o in offers:
        ev = o.evaluation or {}
        radar = {DIM_LABELS[d]: ev.get(d, 3) for d in dims}
        # 综合指数：薪资归一化 40% + 各主观维度 60%
        subj = sum(ev.get(d, 3) for d in dims if d != "salary") / 5
        salary_norm = (o.total_annual or 0) / max_total * 5
        recommend = round((salary_norm * 0.4 + subj * 0.6 / 5 * 5 * 0.6 + subj * 0.6) / 1.2, 1)
        recommend = round(min(10, (salary_norm / 5 * 4) + (subj / 5 * 6)), 1)
        result.append({
            "id": o.id, "company_name": o.company_name, "position_title": o.position_title,
            "total_annual": o.total_annual, "work_city": o.work_city, "radar": radar,
            "recommend_index": recommend,
        })
    result.sort(key=lambda x: x["recommend_index"], reverse=True)
    return result
