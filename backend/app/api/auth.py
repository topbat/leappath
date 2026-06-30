"""认证：登录 / 注册 / 当前用户。演示模式下可直接用演示账号体验。"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.core.serialize import model_to_dict
from app.models.user import UsrUser

router = APIRouter(prefix="/api/auth", tags=["认证"])


class LoginIn(BaseModel):
    account: str  # email / phone
    password: str


class RegisterIn(BaseModel):
    account: str
    password: str
    nickname: str | None = None


def _public(user: UsrUser) -> dict:
    return model_to_dict(user, exclude={"password_hash"})


@router.post("/login")
def login(body: LoginIn, db: Session = Depends(get_db)):
    user = (
        db.query(UsrUser)
        .filter((UsrUser.email == body.account) | (UsrUser.phone == body.account))
        .first()
    )
    if not user or not user.password_hash or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=400, detail="账号或密码错误")
    return {"token": create_access_token(user.id), "user": _public(user)}


@router.post("/register")
def register(body: RegisterIn, db: Session = Depends(get_db)):
    exists = db.query(UsrUser).filter(UsrUser.email == body.account).first()
    if exists:
        raise HTTPException(status_code=400, detail="该账号已注册")
    user = UsrUser(
        email=body.account,
        password_hash=hash_password(body.password),
        nickname=body.nickname or "求职者",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_access_token(user.id), "user": _public(user)}


@router.get("/me")
def me(user: UsrUser = Depends(get_current_user)):
    return _public(user)


@router.put("/me")
def update_me(body: dict, user: UsrUser = Depends(get_current_user), db: Session = Depends(get_db)):
    editable = {
        "nickname", "avatar_url", "gender", "birth_year", "current_city", "target_cities",
        "education_level", "years_of_experience", "current_industry", "target_industries",
        "target_positions", "expected_salary_min", "expected_salary_max",
    }
    for k, v in body.items():
        if k in editable:
            setattr(user, k, v)
    db.commit()
    db.refresh(user)
    return _public(user)
