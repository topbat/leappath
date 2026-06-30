# 求职助手 — 数据模型设计

> 版本：v1.0  
> 更新日期：2026-06-25  
> 数据库：PostgreSQL + Redis（缓存）

---

## 1. ER 总览

```
┌──────────┐    1:N    ┌────────────┐    1:N    ┌─────────────────┐
│   User   │──────────│   Resume   │──────────│  ResumeSection   │
└──────────┘          └────────────┘          └─────────────────┘
     │ 1:N                  │ 1:N
     │              ┌───────┴───────┐
     │              │ ResumeVersion │
     │              └───────────────┘
     │
     │ 1:N    ┌────────────────┐    1:N    ┌─────────────────┐
     ├───────│ JobApplication │──────────│   JobPosition    │
     │        └────────────────┘          └─────────────────┘
     │                                            │ N:1
     │                                    ┌───────┴───────┐
     │                                    │    Company     │
     │                                    └───────────────┘
     │ 1:N    ┌──────────────────┐    1:N    ┌─────────────────┐
     ├───────│ InterviewSession │──────────│ InterviewMessage │
     │        └──────────────────┘          └─────────────────┘
     │               │ 1:1
     │        ┌──────┴───────┐
     │        │InterviewReport│
     │        └──────────────┘
     │
     │ 1:1    ┌────────────┐
     ├───────│ CareerPlan  │
     │        └────────────┘
     │ 1:N    ┌────────────┐
     ├───────│ DailyTask   │
     │        └────────────┘
     │
     │ 1:N    ┌────────────────┐
     ├───────│ OfferRecord    │
     │        └────────────────┘
     │
     │ N:M    ┌────────────────┐
     ════════│ UserSavedCompany│
              └────────────────┘
```

---

## 2. 核心表结构

### 2.1 用户模块

#### user（用户表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | 用户唯一标识 |
| wechat_openid | VARCHAR(64) | UNIQUE, NULLABLE | 微信 OpenID |
| wechat_unionid | VARCHAR(64) | NULLABLE | 微信 UnionID |
| phone | VARCHAR(20) | NULLABLE | 手机号 |
| email | VARCHAR(255) | NULLABLE | 邮箱 |
| nickname | VARCHAR(50) | NOT NULL | 昵称 |
| avatar_url | VARCHAR(500) | | 头像 URL |
| gender | SMALLINT | | 0=未知 1=男 2=女 |
| birth_year | SMALLINT | | 出生年份 |
| current_city | VARCHAR(50) | | 当前城市 |
| target_cities | JSONB | | 目标城市列表 |
| education_level | VARCHAR(20) | | 最高学历 |
| years_of_experience | SMALLINT | | 工作年限 |
| current_industry | VARCHAR(50) | | 当前行业 |
| target_industries | JSONB | | 目标行业列表 |
| target_positions | JSONB | | 目标职位列表 |
| expected_salary_min | INTEGER | | 期望薪资下限 |
| expected_salary_max | INTEGER | | 期望薪资上限 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否激活 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_user_wechat_openid`, `idx_user_phone`, `idx_user_email`

---

### 2.2 简历模块

#### resume（简历主表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | 所属用户 |
| title | VARCHAR(100) | NOT NULL | 简历标题（如"默认简历"） |
| is_default | BOOLEAN | DEFAULT FALSE | 是否默认简历 |
| template_id | VARCHAR(50) | | 模板标识 |
| status | VARCHAR(20) | DEFAULT 'draft' | draft/complete/archived |
| score_total | SMALLINT | | 综合评分 0-100 |
| score_breakdown | JSONB | | 各维度评分详情 |
| source_file_url | VARCHAR(500) | | 原始上传文件路径 |
| parsed_data | JSONB | | 原始解析数据 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_resume_user_id`, `idx_resume_status`

#### resume_section（简历模块）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| resume_id | UUID | FK → resume.id | |
| section_type | VARCHAR(30) | NOT NULL | personal_info/education/experience/project/skill/certificate/language/self_evaluation |
| sort_order | SMALLINT | NOT NULL | 排序 |
| content | JSONB | NOT NULL | 结构化内容 |
| ai_suggestions | JSONB | | AI 润色建议 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_resume_section_resume_id`, `idx_resume_section_type`

#### resume_version（简历版本）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| resume_id | UUID | FK → resume.id | 基于哪个主简历 |
| version_name | VARCHAR(100) | NOT NULL | 版本名称（如"腾讯-后端"） |
| target_company | VARCHAR(100) | | 目标公司 |
| target_position | VARCHAR(100) | | 目标职位 |
| target_jd_text | TEXT | | 目标 JD 原文 |
| snapshot_data | JSONB | NOT NULL | 版本快照（完整简历数据） |
| match_score | SMALLINT | | 与目标 JD 匹配度 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_resume_version_resume_id`

---

### 2.3 职位与投递模块

#### company（公司表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| name | VARCHAR(200) | NOT NULL | 公司全称 |
| short_name | VARCHAR(50) | | 简称 |
| logo_url | VARCHAR(500) | | Logo |
| industry | VARCHAR(50) | | 行业 |
| size_range | VARCHAR(20) | | 规模：<50/50-200/200-500/500-1000/1000-5000/5000+ |
| financing_stage | VARCHAR(20) | | 融资阶段：angel/A/B/C/D/listed |
| location_city | VARCHAR(50) | | 总部城市 |
| location_address | VARCHAR(300) | | 详细地址 |
| location_coord | POINT | | 经纬度（PostGIS） |
| description | TEXT | | 公司简介 |
| website | VARCHAR(300) | | 官网 |
| tech_stack | JSONB | | 技术栈 |
| culture_tags | JSONB | | 文化标签 |
| difficulty_level | VARCHAR(10) | | 求职难度：low/medium/high/extreme |
| data_source | VARCHAR(30) | | 数据来源 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_company_name`, `idx_company_industry`, `idx_company_city`, `idx_company_coord` (GIST)

#### company_salary（公司薪资数据）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| company_id | UUID | FK → company.id | |
| position_name | VARCHAR(100) | NOT NULL | 岗位名称 |
| salary_min | INTEGER | | 最低月薪 |
| salary_max | INTEGER | | 最高月薪 |
| salary_avg | INTEGER | | 平均月薪 |
| bonus_months | SMALLINT | | 年终奖月数 |
| stock_option | VARCHAR(100) | | 期权/股票描述 |
| sample_count | INTEGER | | 样本数量 |
| data_year | SMALLINT | | 数据年份 |
| data_source | VARCHAR(30) | | 来源 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_company_salary_company`, `idx_company_salary_position`

#### company_review（公司评价/面经）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| company_id | UUID | FK → company.id | |
| review_type | VARCHAR(20) | NOT NULL | interview/employee |
| position_name | VARCHAR(100) | | 面试岗位 |
| interview_round | VARCHAR(20) | | 面试轮次 |
| interview_difficulty | SMALLINT | | 难度 1-5 |
| interview_questions | JSONB | | 面试问题列表 |
| review_content | TEXT | | 评价内容 |
| offer_result | VARCHAR(20) | | 结果：offer/rejected/withdrawn |
| publish_date | DATE | | 发布日期 |
| data_source | VARCHAR(30) | | 来源平台 |
| source_url | VARCHAR(500) | | 原文链接 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_company_review_company`, `idx_company_review_type`

#### job_position（职位表）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| company_id | UUID | FK → company.id | |
| title | VARCHAR(200) | NOT NULL | 职位名称 |
| department | VARCHAR(100) | | 部门 |
| location_city | VARCHAR(50) | | 工作城市 |
| location_district | VARCHAR(50) | | 区 |
| salary_min | INTEGER | | |
| salary_max | INTEGER | | |
| salary_period | VARCHAR(10) | | month/year |
| experience_required | VARCHAR(20) | | 经验要求 |
| education_required | VARCHAR(20) | | 学历要求 |
| job_description | TEXT | NOT NULL | JD 原文 |
| job_requirements | TEXT | | 任职要求 |
| job_tags | JSONB | | 职位标签 |
| job_type | VARCHAR(20) | | fulltime/intern/contract |
| source_platform | VARCHAR(30) | | 来源平台 |
| source_url | VARCHAR(500) | | 原始链接 |
| source_id | VARCHAR(100) | | 原始 ID |
| posted_date | DATE | | 发布日期 |
| expire_date | DATE | | 过期日期 |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_job_position_company`, `idx_job_position_title`, `idx_job_position_city`, `idx_job_position_active`

#### job_application（投递记录）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| position_id | UUID | FK → job_position.id | NULLABLE（手动添加时可能为空） |
| resume_version_id | UUID | FK → resume_version.id | 使用的简历版本 |
| company_name | VARCHAR(200) | NOT NULL | 冗余，方便显示 |
| position_title | VARCHAR(200) | NOT NULL | 冗余 |
| status | VARCHAR(20) | NOT NULL | saved/applied/screening/interview/offer/accepted/rejected |
| applied_date | DATE | | 投递日期 |
| next_follow_up | DATE | | 下次跟进日期 |
| notes | TEXT | | 备注 |
| interviews | JSONB | | 面试安排 [{date, type, contact, notes}] |
| status_history | JSONB | | 状态变更历史 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_application_user`, `idx_application_status`, `idx_application_date`

#### user_saved_company（收藏公司）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| company_id | UUID | FK → company.id | |
| notes | TEXT | | 个人备注 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**唯一约束：** UNIQUE(user_id, company_id)

---

### 2.4 模拟面试模块

#### interview_session（面试会话）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| resume_id | UUID | FK → resume.id | NULLABLE | 关联的简历 |
| interview_type | VARCHAR(20) | NOT NULL | technical/behavioral/hr/group/case |
| industry | VARCHAR(50) | | 行业 |
| position | VARCHAR(100) | | 目标职位 |
| company_name | VARCHAR(200) | | 目标公司 |
| difficulty | VARCHAR(10) | DEFAULT 'medium' | easy/medium/hard |
| status | VARCHAR(20) | DEFAULT 'in_progress' | in_progress/completed/abandoned |
| started_at | TIMESTAMPTZ | DEFAULT NOW() | |
| completed_at | TIMESTAMPTZ | | |
| duration_seconds | INTEGER | | 总时长 |

**索引：** `idx_interview_session_user`, `idx_interview_session_status`

#### interview_message（面试消息）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| session_id | UUID | FK → interview_session.id | |
| role | VARCHAR(10) | NOT NULL | interviewer/user/system |
| message_type | VARCHAR(20) | DEFAULT 'text' | text/voice/feedback |
| content | TEXT | NOT NULL | 消息内容 |
| question_number | SMALLINT | | 第几题 |
| feedback | JSONB | | 该轮反馈（AI 角色消息附带） |
| token_count | INTEGER | | Token 用量 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_interview_message_session`

#### interview_report（面试报告）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| session_id | UUID | FK → interview_session.id | UNIQUE |
| overall_score | SMALLINT | | 综合评分 1-10 |
| score_breakdown | JSONB | | 各维度评分 |
| strengths | JSONB | | 优势列表 |
| weaknesses | JSONB | | 短板列表 |
| suggestions | JSONB | | 提升建议 |
| question_reviews | JSONB | | 逐题回顾和评价 |
| summary | TEXT | | 综合评价 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

---

### 2.5 求职规划模块

#### career_plan（求职规划）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | UNIQUE |
| target_industry | VARCHAR(50) | | |
| target_position | VARCHAR(100) | | |
| target_start_date | DATE | | 目标入职日期 |
| timeline | JSONB | | 时间线 [{phase, start, end, tasks}] |
| current_progress | SMALLINT | | 整体进度 0-100 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### skill_assessment（能力评估）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| assessment_type | VARCHAR(20) | | self/ai |
| skills | JSONB | | [{name, category, self_score, ai_score, target_score}] |
| radar_chart_data | JSONB | | 雷达图数据 |
| gap_analysis | JSONB | | 差距分析 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_skill_assessment_user`

#### learning_path（学习路径）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| skill_name | VARCHAR(100) | NOT NULL | 目标技能 |
| resources | JSONB | | [{type, title, url, duration, priority}] |
| estimated_hours | INTEGER | | 预估总时长 |
| completed_hours | INTEGER | DEFAULT 0 | |
| status | VARCHAR(20) | DEFAULT 'in_progress' | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### daily_task（每日任务）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| task_date | DATE | NOT NULL | 任务日期 |
| task_type | VARCHAR(30) | | apply/study/practice/interview/other |
| title | VARCHAR(200) | NOT NULL | |
| description | TEXT | | |
| is_completed | BOOLEAN | DEFAULT FALSE | |
| completed_at | TIMESTAMPTZ | | |
| sort_order | SMALLINT | | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_daily_task_user_date`, `idx_daily_task_user_completed`

---

### 2.6 求职准备模块

#### question_bank（题库）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| category | VARCHAR(30) | NOT NULL | common/technical/aptitude/personality |
| sub_category | VARCHAR(50) | | 前端/后端/算法/产品/... |
| difficulty | VARCHAR(10) | DEFAULT 'medium' | |
| question | TEXT | NOT NULL | 问题 |
| answer | TEXT | | 参考答案 |
| answer_tips | JSONB | | 答题要点 |
| tags | JSONB | | 标签 |
| source | VARCHAR(100) | | 来源 |
| use_count | INTEGER | DEFAULT 0 | 被使用次数 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_question_bank_category`, `idx_question_bank_difficulty`

#### practice_record（练习记录）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| question_id | UUID | FK → question_bank.id | NULLABLE |
| question_text | TEXT | | 自定义问题 |
| user_answer | TEXT | | |
| ai_feedback | JSONB | | AI 批改反馈 |
| score | SMALLINT | | 自评/ AI 评分 |
| time_spent_seconds | INTEGER | | 耗时 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_practice_record_user`, `idx_practice_record_question`

#### offer_record（Offer 记录）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| company_name | VARCHAR(200) | NOT NULL | |
| position_title | VARCHAR(200) | NOT NULL | |
| base_salary | INTEGER | | 月 base |
| bonus_months | SMALLINT | | 年终奖月数 |
| stock_value | INTEGER | | 期权/股票年化价值 |
| other_benefits | JSONB | | 其他福利 |
| total_annual | INTEGER | | 总包年薪 |
| work_city | VARCHAR(50) | | |
| commute_time | INTEGER | | 通勤时间（分钟） |
| evaluation | JSONB | | 多维度评估 |
| is_accepted | BOOLEAN | | 是否接受 |
| notes | TEXT | | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_offer_record_user`

---

### 2.7 租房选址模块

#### rental_listing（房源）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| title | VARCHAR(300) | NOT NULL | 房源标题 |
| city | VARCHAR(50) | NOT NULL | 城市 |
| district | VARCHAR(50) | | 区 |
| community_name | VARCHAR(200) | | 小区名称 |
| address | VARCHAR(500) | | 详细地址 |
| coord | POINT | NOT NULL | 经纬度（PostGIS） |
| price_monthly | INTEGER | NOT NULL | 月租金 |
| price_deposit | VARCHAR(20) | | 押金方式 |
| room_type | VARCHAR(20) | | 户型：studio/1room/2room/3room/4room+ |
| rent_type | VARCHAR(10) | | whole/share（整租/合租） |
| area_sqm | DECIMAL(6,2) | | 面积 |
| floor_level | VARCHAR(10) | | low/mid/high |
| total_floors | SMALLINT | | 总楼层 |
| orientation | VARCHAR(10) | | 朝向 |
| decoration | VARCHAR(10) | | 装修：fine/simple/rough |
| has_elevator | BOOLEAN | | |
| has_balcony | BOOLEAN | | |
| has_private_bath | BOOLEAN | | 独立卫生间 |
| images | JSONB | | 图片 URL 列表 |
| facilities | JSONB | | 配套设施 |
| nearby_poi | JSONB | | 周边 POI |
| contact_phone | VARCHAR(20) | | 联系方式（脱敏） |
| source_platform | VARCHAR(30) | | 来源 |
| source_url | VARCHAR(500) | | 原始链接 |
| source_id | VARCHAR(100) | | 原始 ID |
| listed_date | DATE | | 上架日期 |
| is_active | BOOLEAN | DEFAULT TRUE | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_rental_coord` (GIST), `idx_rental_city`, `idx_rental_price`, `idx_rental_room_type`

#### commute_analysis（通勤分析缓存）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| from_coord | POINT | NOT NULL | 起点（房源） |
| to_coord | POINT | NOT NULL | 终点（公司） |
| transport_mode | VARCHAR(10) | NOT NULL | walk/subway/drive |
| duration_minutes | INTEGER | | 通勤时间 |
| distance_meters | INTEGER | | 距离 |
| route_detail | JSONB | | 路线详情 |
| cached_at | TIMESTAMPTZ | DEFAULT NOW() | |
| expire_at | TIMESTAMPTZ | | 过期时间 |

**唯一约束：** UNIQUE(from_coord, to_coord, transport_mode)

---

### 2.8 系统辅助表

#### user_quota（用户配额）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | UNIQUE |
| resume_optimize_count | INTEGER | DEFAULT 0 | 简历润色次数 |
| mock_interview_count | INTEGER | DEFAULT 0 | 模拟面试次数 |
| interview_quota_total | INTEGER | DEFAULT 10 | 每月面试配额 |
| interview_quota_used | INTEGER | DEFAULT 0 | 本月已用 |
| quota_reset_date | DATE | | 配额重置日期 |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() | |

#### ai_generation_log（AI 调用日志）

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | UUID | PK | |
| user_id | UUID | FK → user.id | |
| gen_type | VARCHAR(30) | NOT NULL | resume_optimize/interview/interview_feedback/resume_score/... |
| prompt_tokens | INTEGER | | |
| completion_tokens | INTEGER | | |
| model | VARCHAR(50) | | 模型名称 |
| duration_ms | INTEGER | | 耗时 |
| success | BOOLEAN | | |
| error_message | TEXT | | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() | |

**索引：** `idx_ai_log_user`, `idx_ai_log_type`, `idx_ai_log_created`

---

## 3. Redis 缓存设计

| Key 模式 | 类型 | 说明 | TTL |
|---------|------|------|------|
| `session:{token}` | String | 用户登录会话 | 7d |
| `user:{id}:profile` | Hash | 用户基本信息缓存 | 1h |
| `resume:{id}:data` | String | 简历完整数据 | 1h |
| `job:hot:{city}` | List | 热门职位缓存 | 30min |
| `rental:heatmap:{city}` | String | 租金热力图数据 | 6h |
| `commute:{hash}` | String | 通勤分析结果 | 24h |
| `rate_limit:{user_id}:{action}` | String | 接口限流 | 1min |
| `interview:{session_id}:context` | String | 面试对话上下文 | 2h |

---

## 4. 数据关系说明

### 简历版本与 JD 匹配

```
Resume ──→ ResumeVersion ──→ 快照数据
                               │
JobPosition ──→ JD 文本 ──────→ AI 匹配计算 ──→ match_score
```

### 面试上下文

```
InterviewSession ──→ InterviewMessage (按时间序)
                         │
                         ├── 用户消息 (role=user)
                         ├── AI 消息 (role=interviewer, 含 feedback)
                         └── 系统消息 (role=system)
                                     │
                                     └──→ InterviewReport (总结)
```

### 公司数据聚合

```
Company ──┬── CompanySalary (按岗位)
          ├── CompanyReview (面经/评价)
          └── JobPosition (在招职位)
```

---

## 5. 扩展性考虑

- **JSONB 字段**：对频繁变更的结构（如评分详情、技能标签、面经列表）使用 JSONB，避免频繁 DDL
- **PostGIS**：租房选址和通勤分析使用 PostGIS 空间索引，支持高效的地理查询
- **数据分区**：`ai_generation_log`、`interview_message` 等大表按时间分区
- **读写分离**：读多写少的查询（职位浏览、公司查看）可走只读副本