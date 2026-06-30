"""首页 Dashboard 聚合接口。"""
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.serialize import models_to_list
from app.models.interview import ItvSession
from app.models.job import JobApplication
from app.models.plan import PlnDailyTask, PlnPlan
from app.models.resume import RsmResume
from app.models.user import UsrUser

router = APIRouter(prefix="/api/dashboard", tags=["首页"])


@router.get("")
def dashboard(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    resumes = db.query(RsmResume).filter(RsmResume.user_id == user.id).all()
    apps = db.query(JobApplication).filter(JobApplication.user_id == user.id).all()
    interviews = db.query(ItvSession).filter(ItvSession.user_id == user.id).all()
    tasks = db.query(PlnDailyTask).filter(
        PlnDailyTask.user_id == user.id, PlnDailyTask.task_date == date.today()
    ).order_by(PlnDailyTask.sort_order).all()
    plan = db.query(PlnPlan).filter(PlnPlan.user_id == user.id).first()

    # 投递统计
    stat = {}
    for a in apps:
        stat[a.status] = stat.get(a.status, 0) + 1

    # 模块完成度（估算）
    best_resume = max((r.score_total or 0 for r in resumes), default=0)
    resume_progress = best_resume
    interview_progress = min(100, len([i for i in interviews if i.status == "completed"]) * 25)
    completed_tasks = len([t for t in tasks if t.is_completed])
    skill_progress = plan.current_progress if plan else 50
    overall = round((resume_progress + interview_progress + skill_progress) / 3)

    return {
        "user": {"nickname": user.nickname, "avatar_url": user.avatar_url},
        "progress": {
            "overall": overall,
            "resume": resume_progress,
            "interview": interview_progress,
            "skill": skill_progress,
        },
        "application_stats": {
            "saved": stat.get("saved", 0),
            "applied": stat.get("applied", 0),
            "screening": stat.get("screening", 0),
            "interview": stat.get("interview", 0),
            "offer": stat.get("offer", 0) + stat.get("accepted", 0),
            "rejected": stat.get("rejected", 0),
            "total": len(apps),
        },
        "today_tasks": models_to_list(tasks),
        "today_task_done": completed_tasks,
        "counts": {
            "resumes": len(resumes),
            "interviews": len(interviews),
            "applications": len(apps),
        },
        "target_start_date": plan.target_start_date.isoformat() if plan and plan.target_start_date else None,
    }
