"""求职规划：规划、能力评估、学习路径、每日任务、进度看板。"""
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db, now_utc
from app.core.deps import get_current_user
from app.core.serialize import model_to_dict, models_to_list
from app.models.plan import PlnDailyTask, PlnLearningPath, PlnPlan, PlnSkillAssessment
from app.models.user import UsrUser
from app.services import ai

router = APIRouter(prefix="/api/plan", tags=["求职规划"])


@router.get("")
def get_plan(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(PlnPlan).filter(PlnPlan.user_id == user.id).first()
    if not p:
        p = PlnPlan(user_id=user.id, current_progress=0, timeline=[])
        db.add(p)
        db.commit()
        db.refresh(p)
    return model_to_dict(p)


@router.put("")
def update_plan(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    p = db.query(PlnPlan).filter(PlnPlan.user_id == user.id).first()
    if not p:
        p = PlnPlan(user_id=user.id)
        db.add(p)
    for k in ("target_industry", "target_position", "timeline", "current_progress"):
        if k in body:
            setattr(p, k, body[k])
    if body.get("target_start_date"):
        p.target_start_date = date.fromisoformat(body["target_start_date"])
        # 倒推生成时间线
        if not body.get("timeline"):
            p.timeline = _build_timeline(p.target_start_date)
    db.commit()
    db.refresh(p)
    return model_to_dict(p)


def _build_timeline(target: date) -> list:
    return [
        {"phase": "准备期", "desc": "简历优化 · 技能提升 · 模拟面试", "weeks_before": 12},
        {"phase": "投递期", "desc": "精准投递 · 跟进反馈", "weeks_before": 8},
        {"phase": "密集面试期", "desc": "多轮面试 · 复盘提升", "weeks_before": 4},
        {"phase": "Offer 谈判期", "desc": "薪资谈判 · Offer 对比", "weeks_before": 2},
        {"phase": "入职", "desc": "背调 · 租房选址 · 入职准备", "weeks_before": 0},
    ]


# ---------- 能力评估 ----------

@router.post("/assessment")
def create_assessment(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    skills = body.get("skills", [])
    result = ai.assess_skills(skills, body.get("target_position"))
    a = PlnSkillAssessment(
        user_id=user.id,
        assessment_type=body.get("assessment_type", "self"),
        skills=skills,
        radar_chart_data={"radar": result["radar"]},
        gap_analysis=result["gaps"],
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    d = model_to_dict(a)
    return d


@router.get("/assessment")
def latest_assessment(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    a = db.query(PlnSkillAssessment).filter(PlnSkillAssessment.user_id == user.id).order_by(PlnSkillAssessment.created_at.desc()).first()
    return model_to_dict(a) if a else None


# ---------- 学习路径 ----------

@router.get("/learning")
def list_learning(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(PlnLearningPath).filter(PlnLearningPath.user_id == user.id).all()
    return models_to_list(items)


@router.post("/learning")
def create_learning(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    lp = PlnLearningPath(
        user_id=user.id,
        skill_name=body.get("skill_name", "目标技能"),
        resources=body.get("resources", []),
        estimated_hours=body.get("estimated_hours", 20),
    )
    db.add(lp)
    db.commit()
    db.refresh(lp)
    return model_to_dict(lp)


# ---------- 每日任务 ----------

@router.get("/tasks")
def list_tasks(task_date: str | None = None, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    q = db.query(PlnDailyTask).filter(PlnDailyTask.user_id == user.id)
    if task_date:
        q = q.filter(PlnDailyTask.task_date == date.fromisoformat(task_date))
    else:
        q = q.filter(PlnDailyTask.task_date == date.today())
    items = q.order_by(PlnDailyTask.sort_order).all()
    return models_to_list(items)


@router.post("/tasks")
def create_task(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    t = PlnDailyTask(
        user_id=user.id,
        task_date=date.fromisoformat(body["task_date"]) if body.get("task_date") else date.today(),
        task_type=body.get("task_type", "other"),
        title=body.get("title", "新任务"),
        description=body.get("description"),
        sort_order=body.get("sort_order", 0),
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return model_to_dict(t)


@router.put("/tasks/{tid}")
def update_task(tid: str, body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    t = db.get(PlnDailyTask, tid)
    if not t or t.user_id != user.id:
        raise HTTPException(404, "任务不存在")
    if "is_completed" in body:
        t.is_completed = body["is_completed"]
        t.completed_at = now_utc() if body["is_completed"] else None
    for k in ("title", "description", "task_type", "sort_order"):
        if k in body:
            setattr(t, k, body[k])
    db.commit()
    db.refresh(t)
    return model_to_dict(t)


@router.delete("/tasks/{tid}")
def delete_task(tid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    t = db.get(PlnDailyTask, tid)
    if not t or t.user_id != user.id:
        raise HTTPException(404, "任务不存在")
    db.delete(t)
    db.commit()
    return {"ok": True}
