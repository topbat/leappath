"""Mock AI 服务。

为保证「开箱即跑、无需任何 API Key」，这里用确定性的规则/模板模拟 AI 能力：
简历润色、简历评分、面试出题/追问/反馈、面试报告、JD 匹配度、技能差距等。
真实接入时，仅需把每个函数内部替换为对 Claude API 的调用即可，接口签名保持不变。
"""
from __future__ import annotations

import hashlib
import re
from typing import Any

# ---------- 通用工具 ----------

def _seed(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)


def _pick(text: str, options: list) -> Any:
    return options[_seed(text) % len(options)]


def _score_from(text: str, lo: int, hi: int) -> int:
    return lo + _seed(text) % (hi - lo + 1)


# ---------- 简历润色 ----------

_STYLE_LABEL = {
    "professional": "专业严谨",
    "concise": "简洁有力",
    "data": "数据驱动",
}

_QUANT_HINTS = ["30%", "40%", "2 倍", "1500 → 4200", "60%", "3 倍"]


def polish_resume_item(original: str, style: str = "professional", target: str | None = None) -> dict:
    """对单条经历做 STAR 化润色。仅基于原文改写，不编造，量化值标记为待确认。"""
    style_label = _STYLE_LABEL.get(style, "专业严谨")
    quant = _pick(original, _QUANT_HINTS)
    verb = _pick(original + style, ["主导", "负责并推动", "牵头", "独立完成"])
    base = original.strip().rstrip("。.")
    polished = (
        f"{verb}{base}：明确目标与场景（S/T），通过系统性的方案设计与落地（A），"
        f"最终取得可量化的成果（R），关键指标提升约 {quant}（数值待你确认）。"
    )
    if style == "concise":
        polished = f"{verb}{base}，成果显著（约 {quant}，待确认）。"
    elif style == "data":
        polished = f"{verb}{base}，核心指标实现 {quant} 的提升（数值待你确认），并沉淀为可复用方案。"
    return {
        "original": original,
        "polished": polished,
        "style": style,
        "style_label": style_label,
        "needs_confirm": [quant],
        "notes": "已套用 STAR 法则改写，量化数值为占位，请按真实情况确认。",
    }


# ---------- 简历评分 ----------

_DIMENSIONS = [
    ("completeness", "内容完整度", 25),
    ("keyword", "关键词匹配", 25),
    ("format", "格式规范", 15),
    ("competitiveness", "竞争力", 25),
    ("aigc", "AIGC 检测", 10),
]


def score_resume(resume_title: str, sections: list[dict], target: str | None = None) -> dict:
    body = resume_title + "|" + "|".join(s.get("section_type", "") for s in sections)
    breakdown = {}
    total = 0.0
    for key, label, weight in _DIMENSIONS:
        s = _score_from(body + key, 60, 96)
        # 内容越全分越高
        if key == "completeness":
            s = min(98, 50 + len(sections) * 8)
        breakdown[key] = {"label": label, "score": s, "weight": weight}
        total += s * weight / 100.0
    total = round(total)
    suggestions = [
        {"level": "critical", "text": "工作经历缺少量化成果，建议补充具体数据指标（QPS、转化率、节省成本等）。"},
        {"level": "suggest", "text": "技能标签与目标岗位匹配度偏低，建议结合 JD 补充 2-3 个核心关键词。"},
        {"level": "optimize", "text": "自我评价偏模板化，建议结合个人亮点个性化改写。"},
        {"level": "optimize", "text": "建议补充 1-2 个有深度、可量化的重点项目经验。"},
    ]
    grade = "优秀" if total >= 85 else "良好" if total >= 70 else "待提升"
    return {"score_total": total, "grade": grade, "breakdown": breakdown, "suggestions": suggestions}


def match_jd(resume_text: str, jd_text: str) -> dict:
    """简历 × JD 多维匹配度。"""
    jd_keywords = _extract_keywords(jd_text)
    resume_lower = resume_text.lower()
    matched, missing = [], []
    for kw in jd_keywords:
        (matched if kw.lower() in resume_lower else missing).append(kw)
    dims = {
        "skill": min(99, 40 + len(matched) * 12),
        "experience": _score_from(resume_text + "exp", 55, 95),
        "education": _score_from(resume_text + "edu", 60, 98),
        "salary": _score_from(resume_text + "sal", 55, 95),
        "location": _score_from(resume_text + "loc", 60, 99),
    }
    overall = round(sum(dims.values()) / len(dims))
    gaps = [
        {"point": kw, "level": "critical", "suggestion": f"补齐「{kw}」相关项目或学习经历，可在简历技能区与经历区各体现一次。"}
        for kw in missing[:4]
    ]
    return {
        "overall": overall,
        "level": "high" if overall >= 80 else "medium" if overall >= 60 else "low",
        "dimensions": dims,
        "matched": matched[:8],
        "missing": missing[:8],
        "gaps": gaps,
    }


_STOP = {"的", "和", "与", "及", "等", "the", "and", "or", "a", "an", "to", "of", "in", "for", "经验", "熟悉", "了解", "优先"}


def _extract_keywords(text: str) -> list[str]:
    tokens = re.split(r"[\s,，、。.;；:：/|\\(\)\[\]【】]+", text)
    seen, out = set(), []
    for t in tokens:
        t = t.strip()
        if 2 <= len(t) <= 12 and t.lower() not in _STOP and t not in seen:
            seen.add(t)
            out.append(t)
    return out[:12]


# ---------- 模拟面试 ----------

_QUESTION_BANK = {
    "technical": [
        "请先做个自我介绍，重点说说你最擅长的技术领域。",
        "请描述一下你在项目中遇到的最有挑战性的技术问题，以及你是如何解决的？",
        "如果让你设计一个高并发的短链系统，你会如何考虑存储与缓存？",
        "你提到的性能优化，具体是怎么定位瓶颈的？用了哪些手段？",
        "说说你对你主力技术栈底层原理的理解。",
        "如果线上出现一次 P0 故障，你的排查思路是怎样的？",
        "你做过哪些工程化或团队效率方面的改进？",
        "聊聊你近期在学习的新技术，为什么关注它？",
    ],
    "behavioral": [
        "请做个自我介绍。",
        "讲一个你和同事产生分歧、最终推动达成一致的经历（STAR）。",
        "描述一次你在压力下完成目标的经历。",
        "你遇到过最大的失败是什么？从中学到了什么？",
        "举一个你主动承担额外责任的例子。",
        "你如何平衡多个并行任务的优先级？",
        "讲一次你帮助团队改进流程的经历。",
        "未来三年你的职业规划是怎样的？",
    ],
    "hr": [
        "请简单介绍一下你自己。",
        "你为什么选择我们公司？",
        "你的期望薪资是多少？依据是什么？",
        "你最大的优点和缺点分别是什么？",
        "你离开上一家公司的原因是什么？",
        "你如何看待加班？",
        "你还有什么想问我的吗？",
        "如果同时拿到几个 offer，你会如何选择？",
    ],
}
_QUESTION_BANK["group"] = _QUESTION_BANK["behavioral"]
_QUESTION_BANK["case"] = _QUESTION_BANK["technical"]


def interview_questions(interview_type: str, total: int = 8) -> list[str]:
    pool = _QUESTION_BANK.get(interview_type, _QUESTION_BANK["behavioral"])
    return pool[:total]


_FOLLOW_UPS = [
    "你提到了一个结果，能给出具体的量化数据吗？比如从多少提升到了多少？",
    "这个决策当时还有别的备选方案吗？为什么选了现在这个？",
    "如果重来一次，你会做哪些不同的处理？",
    "在这个过程中，你个人最关键的贡献是什么？",
]


def interview_feedback(answer: str, question_number: int) -> dict:
    """对单轮回答给即时反馈。"""
    length = len(answer.strip())
    has_number = bool(re.search(r"\d", answer))
    on_topic = length >= 20
    star = length >= 60
    tags = []
    tags.append({"type": "good" if on_topic else "warn", "text": "内容切题" if on_topic else "回答略简略"})
    tags.append({"type": "good" if has_number else "warn", "text": "有量化数据" if has_number else "缺少量化数据"})
    tags.append({"type": "good" if star else "tip", "text": "STAR 结构完整" if star else "建议补全 STAR 结构"})
    suggestion = "回答不错，可继续保持结构化表达。" if (on_topic and has_number) else "建议补充具体指标与结果，让回答更有说服力。"
    follow_up = None
    if not has_number or not star:
        follow_up = _pick(answer + str(question_number), _FOLLOW_UPS)
    quality = _score_from(answer, 5, 9) if length else 4
    return {"tags": tags, "suggestion": suggestion, "follow_up": follow_up, "quality": quality}


def interview_report(messages: list[dict], interview_type: str) -> dict:
    answers = [m for m in messages if m.get("role") == "user"]
    joined = " ".join(a.get("content", "") for a in answers) or interview_type
    dims = {
        "communication": _score_from(joined + "c", 5, 9),
        "logic": _score_from(joined + "l", 5, 9),
        "expertise": _score_from(joined + "e", 5, 9),
        "adaptability": _score_from(joined + "a", 5, 9),
    }
    overall = round(sum(dims.values()) / len(dims), 1)
    reviews = []
    for i, a in enumerate(answers, 1):
        reviews.append({
            "question_number": i,
            "score": _score_from(a.get("content", "") + str(i), 5, 9),
            "comment": "回答结构清晰" if len(a.get("content", "")) > 50 else "可补充更多细节",
        })
    return {
        "overall_score": overall,
        "score_breakdown": {
            "沟通表达": dims["communication"],
            "逻辑思维": dims["logic"],
            "专业深度": dims["expertise"],
            "应变能力": dims["adaptability"],
        },
        "strengths": ["项目经验描述清晰，STAR 结构较完整", "技术/业务基础扎实，概念理解准确"],
        "weaknesses": ["部分回答缺少量化数据支撑，建议补充具体指标", "系统设计类问题可进一步补充容灾与扩展性"],
        "suggestions": ["针对高频追问准备 2-3 组量化案例", "练习 1 分钟、3 分钟两个版本的自我介绍", "复盘本次薄弱维度并二刷题库"],
        "question_reviews": reviews,
        "summary": f"本次{_type_label(interview_type)}整体表现{'良好' if overall >= 7 else '中等'}，综合评分 {overall}/10，建议针对量化表达与系统性思考重点提升。",
    }


def _type_label(t: str) -> str:
    return {"technical": "技术面", "behavioral": "行为面", "hr": "HR 面", "group": "群面", "case": "案例面"}.get(t, "面试")


# ---------- 技能评估 / 学习路径 ----------

def assess_skills(skills: list[dict], target_position: str | None = None) -> dict:
    radar = []
    gaps = []
    for s in skills:
        name = s.get("name", "技能")
        self_score = s.get("self_score", _score_from(name, 2, 5))
        target_score = s.get("target_score", 5)
        ai_score = max(1, min(5, self_score + (_seed(name) % 3 - 1)))
        radar.append({"name": name, "self": self_score, "ai": ai_score, "target": target_score})
        if ai_score < target_score:
            level = "critical" if target_score - ai_score >= 2 else "bonus"
            gaps.append({"name": name, "level": level, "gap": target_score - ai_score,
                          "suggestion": f"针对「{name}」安排专项学习与项目实践以缩小差距。"})
    return {"radar": radar, "gaps": gaps}


def negotiation_advice(base_offer: int | None, market_avg: int | None) -> dict:
    return {
        "scripts": [
            "感谢认可！基于我的经验与市场同岗位水平，我对总包的期望在 X 区间，是否有进一步空间？",
            "我非常认同团队和方向，如果 base 暂时受限，能否在签字费/股票/调薪周期上做些补偿？",
        ],
        "strategy": "先锚定总包而非单看 base；用市场数据与竞争 offer 作为支撑；保持合作而非对立的语气。",
        "pitfalls": ["不要第一时间报出底价", "避免只盯 base 忽略期权与年终", "口头承诺务必落到 offer letter"],
    }
