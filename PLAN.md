# 跃途 LeapPath — 开发计划

> 全生命周期 AI 求职助手 · 全栈可运行 MVP
> 技术栈：Vue 3 + Vite + Pinia + Tailwind（双主题可切换） · FastAPI + SQLAlchemy + SQLite · Mock AI 服务

---

## 0. 决策摘要（已与用户确认）

| 项 | 决策 |
|----|------|
| 产品名 | **跃途 LeapPath** |
| 视觉风格 | 两套设计稿都做，运行时主题可切换（`leap` 专业权威蓝 / `flux` 灵动活力紫） |
| 技术栈 | 全栈可运行 MVP：Vue3+Vite 前端 + FastAPI 后端 + SQLAlchemy/SQLite + Mock AI |
| 模块范围 | 全部 7 大模块（含租房地图，地图用占位/Leaflet 演示） |

---

## 1. 数据表前缀规范（按模块区分）

> 要求：不同模块的表使用不同前缀，便于识别与维护。

| 模块 | 前缀 | 表 |
|------|------|----|
| 用户/账户 | `usr_` | usr_user |
| 简历中心 | `rsm_` | rsm_resume, rsm_section, rsm_version |
| 职位/投递 | `job_` | job_position, job_application |
| 公司画像 | `cmp_` | cmp_company, cmp_salary, cmp_review, cmp_user_saved |
| 模拟面试 | `itv_` | itv_session, itv_message, itv_report |
| 求职规划 | `pln_` | pln_plan, pln_skill_assessment, pln_learning_path, pln_daily_task |
| 求职准备 | `prp_` | prp_question_bank, prp_practice_record, prp_offer |
| 租房选址 | `rnt_` | rnt_listing, rnt_commute |
| 系统辅助 | `sys_` | sys_user_quota, sys_ai_log |

每张表内字段沿用 `docs/data-model.md` 设计；SQLite 下用 `String`/`JSON`/`Float` 对应 PostgreSQL 的 UUID/JSONB/POINT。

---

## 2. 目录结构

```
en-job-app/
├── PLAN.md
├── README.md
├── brand/                      # 品牌资产
│   ├── logo.svg / logo-mark.svg / logo-dark.svg
│   └── BRAND.md
├── backend/                    # FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── core/   (config, database, security, deps)
│   │   ├── models/ (按模块拆分，含前缀)
│   │   ├── schemas/
│   │   ├── api/    (按模块路由)
│   │   ├── services/ai.py  (Mock AI)
│   │   └── seed.py
│   └── requirements.txt
└── frontend/                   # Vue3 + Vite
    └── src/
        ├── main.js / App.vue / router / stores
        ├── theme/  (双主题 token + 切换)
        ├── api/
        ├── components/ (common, charts, layout, 业务组件)
        └── pages/      (按模块)
```

## 3. 实施阶段

1. 品牌：名称 + LOGO（SVG）+ BRAND.md
2. 后端基座：app/core（config、database、security、deps）、main、CORS
3. 后端模型（全模块、含前缀）+ Pydantic schemas + Mock AI 服务
4. 后端路由（auth/resume/interview/job/plan/company/prepare/rental/dashboard）+ seed
5. 前端基座：Vite+Vue3+Pinia+Router+Tailwind 双主题 + 布局 + api 封装 + 主题切换
6. 前端 P0 页面：Dashboard、简历中心、模拟面试、职位/投递看板
7. 前端 P1 页面：求职规划、公司画像、求职准备、租房选址
8. 集成、启动前后端、自测主流程、写 README

## 4. 验收标准

- `cd backend && uvicorn app.main:app` 可启动，`/docs` 可见全模块 API，seed 数据可读
- `cd frontend && npm run dev` 可启动，各模块页面可访问、可点通主流程、调用后端
- 顶部可一键切换 `leap`/`flux` 两套主题，整站换肤
- 所有数据表带模块前缀
