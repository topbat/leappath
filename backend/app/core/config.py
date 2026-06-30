"""应用配置。"""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # backend/


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LEAPPATH_", env_file=".env", extra="ignore")

    APP_NAME: str = "跃途 LeapPath API"
    APP_VERSION: str = "1.0.1"
    SECRET_KEY: str = "leappath-dev-secret-change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天
    DATABASE_URL: str = f"sqlite:///{(BASE_DIR / 'leappath.db').as_posix()}"
    # 演示模式：无 token 时自动登录为演示用户，降低体验门槛
    DEMO_MODE: bool = True
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
    ]


settings = Settings()
