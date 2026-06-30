"""ORM -> dict 轻量序列化（含 datetime/date 处理）。"""
from datetime import date, datetime

from sqlalchemy import inspect


def model_to_dict(obj, exclude: set[str] | None = None) -> dict:
    exclude = exclude or set()
    out = {}
    for col in inspect(obj).mapper.column_attrs:
        key = col.key
        if key in exclude:
            continue
        val = getattr(obj, key)
        if isinstance(val, (datetime, date)):
            val = val.isoformat()
        out[key] = val
    return out


def models_to_list(objs, exclude: set[str] | None = None) -> list[dict]:
    return [model_to_dict(o, exclude) for o in objs]
