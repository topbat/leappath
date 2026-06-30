"""模拟面试：会话、消息流（AI 出题/追问/即时反馈）、面试报告。"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db, now_utc
from app.core.deps import get_current_user
from app.core.serialize import model_to_dict, models_to_list
from app.models.interview import ItvMessage, ItvReport, ItvSession
from app.models.user import UsrUser
from app.services import ai

router = APIRouter(prefix="/api/interviews", tags=["模拟面试"])


class SetupIn(BaseModel):
    interview_type: str = "technical"
    industry: str | None = None
    position: str | None = None
    company_name: str | None = None
    difficulty: str = "medium"
    total_questions: int = 8


@router.post("/sessions")
def create_session(body: SetupIn, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    s = ItvSession(
        user_id=user.id,
        interview_type=body.interview_type,
        industry=body.industry,
        position=body.position,
        company_name=body.company_name,
        difficulty=body.difficulty,
        total_questions=body.total_questions,
        status="in_progress",
        started_at=now_utc(),
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    # 推送第一题
    questions = ai.interview_questions(body.interview_type, body.total_questions)
    first = ItvMessage(session_id=s.id, role="interviewer", content=questions[0], question_number=1)
    db.add(first)
    db.commit()
    data = model_to_dict(s)
    data["messages"] = [model_to_dict(first)]
    data["question_pool"] = questions
    return data


@router.get("/sessions")
def list_sessions(user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(ItvSession).filter(ItvSession.user_id == user.id).order_by(ItvSession.created_at.desc()).all()
    return models_to_list(items)


@router.get("/sessions/{sid}")
def get_session(sid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    s = db.get(ItvSession, sid)
    if not s or s.user_id != user.id:
        raise HTTPException(404, "会话不存在")
    msgs = db.query(ItvMessage).filter(ItvMessage.session_id == sid).order_by(ItvMessage.created_at).all()
    data = model_to_dict(s)
    data["messages"] = models_to_list(msgs)
    return data


class AnswerIn(BaseModel):
    content: str


@router.post("/sessions/{sid}/answer")
def answer(sid: str, body: AnswerIn, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    s = db.get(ItvSession, sid)
    if not s or s.user_id != user.id:
        raise HTTPException(404, "会话不存在")
    # 当前题号
    asked = db.query(ItvMessage).filter(ItvMessage.session_id == sid, ItvMessage.role == "interviewer").count()
    fb = ai.interview_feedback(body.content, asked)
    user_msg = ItvMessage(session_id=sid, role="user", content=body.content, question_number=asked, feedback=fb)
    db.add(user_msg)
    db.flush()

    next_msgs = [model_to_dict(user_msg)]
    pool = ai.interview_questions(s.interview_type, s.total_questions)

    if fb.get("follow_up"):
        follow = ItvMessage(session_id=sid, role="interviewer", content=fb["follow_up"], question_number=asked)
        db.add(follow)
        db.flush()
        next_msgs.append(model_to_dict(follow))
    elif asked < s.total_questions:
        nq = ItvMessage(session_id=sid, role="interviewer", content=pool[asked], question_number=asked + 1)
        db.add(nq)
        db.flush()
        next_msgs.append(model_to_dict(nq))
    else:
        s.status = "completed"
        s.completed_at = now_utc()
        sys_msg = ItvMessage(session_id=sid, role="system", content="面试已结束，正在生成报告…", message_type="feedback")
        db.add(sys_msg)
        db.flush()
        next_msgs.append(model_to_dict(sys_msg))

    db.commit()
    return {"feedback": fb, "messages": next_msgs, "status": s.status}


@router.post("/sessions/{sid}/finish")
def finish(sid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    s = db.get(ItvSession, sid)
    if not s or s.user_id != user.id:
        raise HTTPException(404, "会话不存在")
    msgs = db.query(ItvMessage).filter(ItvMessage.session_id == sid).order_by(ItvMessage.created_at).all()
    report_data = ai.interview_report(models_to_list(msgs), s.interview_type)
    existing = db.query(ItvReport).filter(ItvReport.session_id == sid).first()
    if existing:
        db.delete(existing)
        db.flush()
    rep = ItvReport(session_id=sid, **report_data)
    s.status = "completed"
    if not s.completed_at:
        s.completed_at = now_utc()
    if s.started_at:
        s.duration_seconds = int((s.completed_at - s.started_at).total_seconds())
    db.add(rep)
    db.commit()
    db.refresh(rep)
    return model_to_dict(rep)


@router.get("/sessions/{sid}/report")
def get_report(sid: str, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    s = db.get(ItvSession, sid)
    if not s or s.user_id != user.id:
        raise HTTPException(404, "会话不存在")
    rep = db.query(ItvReport).filter(ItvReport.session_id == sid).first()
    if not rep:
        raise HTTPException(404, "报告尚未生成")
    data = model_to_dict(rep)
    data["session"] = model_to_dict(s)
    return data
