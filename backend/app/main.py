"""跃途 LeapPath 后端入口。"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    auth,
    company,
    dashboard,
    interview,
    job,
    plan,
    prepare,
    rental,
    resume,
)
from app.core.config import settings
from app.core.database import init_db

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (auth, dashboard, resume, interview, job, company, plan, prepare, rental):
    app.include_router(r.router)


@app.on_event("startup")
def on_startup():
    init_db()
    from app.seed import seed_if_empty

    seed_if_empty()


@app.get("/")
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "product": "跃途 LeapPath",
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
