"""轻量级 token 与口令哈希（演示用，零额外依赖）。

使用 HMAC 签名的紧凑 token，结构为 base64url(payload).hmac，
避免引入 python-jose / passlib 等额外依赖，保证开箱即跑。
"""
import base64
import hashlib
import hmac
import json
import time

from .config import settings


def _b64e(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64d(data: str) -> bytes:
    pad = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def _sign(payload_b64: str) -> str:
    sig = hmac.new(settings.SECRET_KEY.encode(), payload_b64.encode(), hashlib.sha256).digest()
    return _b64e(sig)


def create_access_token(user_id: str) -> str:
    exp = int(time.time()) + settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    payload_b64 = _b64e(json.dumps({"sub": user_id, "exp": exp}).encode())
    return f"{payload_b64}.{_sign(payload_b64)}"


def decode_access_token(token: str) -> str | None:
    """返回 user_id，失败/过期返回 None。"""
    try:
        payload_b64, sig = token.split(".")
    except ValueError:
        return None
    if not hmac.compare_digest(sig, _sign(payload_b64)):
        return None
    try:
        data = json.loads(_b64d(payload_b64))
    except Exception:
        return None
    if data.get("exp", 0) < int(time.time()):
        return None
    return data.get("sub")


def hash_password(password: str) -> str:
    return hashlib.sha256((settings.SECRET_KEY + password).encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hmac.compare_digest(hash_password(password), hashed)
