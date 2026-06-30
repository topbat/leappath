"""依赖注入：数据库会话与当前用户。"""
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .security import decode_access_token

DEMO_EMAIL = "demo@leappath.app"


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    """从 Bearer token 解析当前用户；演示模式下回退到演示用户。"""
    from app.models.user import UsrUser  # 延迟导入避免循环

    user_id = None
    if authorization and authorization.lower().startswith("bearer "):
        user_id = decode_access_token(authorization[7:])

    if user_id:
        user = db.get(UsrUser, user_id)
        if user:
            return user

    if settings.DEMO_MODE:
        user = db.query(UsrUser).filter(UsrUser.email == DEMO_EMAIL).first()
        if user:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="未登录或登录已过期",
    )
