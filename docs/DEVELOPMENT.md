# 跃途 LeapPath — 开发指南

> **版本**: v1.0.1  
> **更新日期**: 2026-06-30

---

## 📋 目录

- [项目概览](#项目概览)
- [环境搭建](#环境搭建)
- [项目结构](#项目结构)
- [后端开发](#后端开发)
- [前端开发](#前端开发)
- [数据库设计](#数据库设计)
- [API 设计](#api-设计)
- [主题系统](#主题系统)
- [测试指南](#测试指南)
- [代码规范](#代码规范)
- [常见问题](#常见问题)

---

## 项目概览

**跃途 LeapPath** 是一款全生命周期 AI 求职助手，覆盖简历、面试、职位、规划、公司、准备、租房 7 大模块。

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端框架 | Vue 3 + Vite | Composition API + `<script setup>` |
| 状态管理 | Pinia | Vue 3 官方推荐 |
| 路由 | Vue Router 4 | 历史模式 |
| 样式 | Tailwind CSS 3 | 原子化 CSS + 双主题 |
| 后端框架 | FastAPI | 异步 Python Web 框架 |
| ORM | SQLAlchemy 2.0 | 声明式映射 |
| 数据库 | SQLite | 开箱即用，可迁移 PostgreSQL |
| 认证 | HMAC Token | 轻量级，零额外依赖 |

---

## 环境搭建

### 前置条件

```bash
# 检查版本
python --version   # >= 3.10
node --version     # >= 18
npm --version      # >= 8
```

### 1. 克隆项目

```bash
git clone https://github.com/<your-username>/en-job-app.git
cd en-job-app
```

### 2. 后端环境

```bash
cd backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
source .venv/bin/activate      # Linux/Mac
# .venv\Scripts\activate       # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

访问:
- API: http://localhost:8000
- Swagger 文档: http://localhost:8000/docs
- ReDoc 文档: http://localhost:8000/redoc

### 3. 前端环境

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问: http://localhost:5173

### 4. 默认账号

| 项目 | 值 |
|------|-----|
| 邮箱 | `demo@leappath.app` |
| 密码 | `leappath` |

---

## 项目结构

```
en-job-app/
├── .github/workflows/     # CI/CD 配置
├── brand/                 # 品牌资产 (LOGO, 品牌指南)
├── backend/               # 后端 (FastAPI)
│   ├── app/
│   │   ├── main.py        # 应用入口
│   │   ├── core/          # 核心模块
│   │   │   ├── config.py  # 配置管理
│   │   │   ├── database.py # 数据库引擎
│   │   │   ├── security.py # 认证安全
│   │   │   ├── deps.py    # 依赖注入
│   │   │   └── serialize.py # 序列化
│   │   ├── models/        # 数据模型
│   │   │   ├── user.py    # 用户模型
│   │   │   ├── resume.py  # 简历模型
│   │   │   ├── job.py     # 职位模型
│   │   │   ├── company.py # 公司模型
│   │   │   ├── interview.py # 面试模型
│   │   │   ├── plan.py    # 规划模型
│   │   │   ├── prepare.py # 准备模型
│   │   │   ├── rental.py  # 租房模型
│   │   │   └── system.py  # 系统模型
│   │   ├── api/           # API 路由
│   │   │   ├── auth.py    # 认证路由
│   │   │   ├── resume.py  # 简历路由
│   │   │   ├── job.py     # 职位路由
│   │   │   ├── company.py # 公司路由
│   │   │   ├── interview.py # 面试路由
│   │   │   ├── plan.py    # 规划路由
│   │   │   ├── prepare.py # 准备路由
│   │   │   ├── rental.py  # 租房路由
│   │   │   └── dashboard.py # 仪表盘路由
│   │   ├── services/      # 业务服务
│   │   │   └── ai.py      # Mock AI 服务
│   │   └── seed.py        # 种子数据
│   └── requirements.txt
├── frontend/              # 前端 (Vue 3)
│   ├── src/
│   │   ├── main.js        # 入口
│   │   ├── App.vue        # 根组件
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # Pinia 状态管理
│   │   │   ├── user.js    # 用户状态
│   │   │   └── theme.js   # 主题状态
│   │   ├── api/           # API 客户端
│   │   │   └── client.js  # Fetch 封装
│   │   ├── components/    # 组件
│   │   │   ├── common/    # 通用组件
│   │   │   ├── charts/    # 图表组件
│   │   │   └── layout/    # 布局组件
│   │   └── pages/         # 页面
│   │       ├── Dashboard.vue
│   │       ├── Login.vue
│   │       ├── Profile.vue
│   │       ├── resume/    # 简历模块
│   │       ├── interview/ # 面试模块
│   │       ├── jobs/      # 职位模块
│   │       ├── plan/      # 规划模块
│   │       ├── company/   # 公司模块
│   │       ├── prepare/   # 准备模块
│   │       └── rental/    # 租房模块
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── docs/                  # 文档
│   ├── PRD.md             # 产品需求文档
│   ├── DEPLOYMENT.md      # 部署指南
│   ├── DEVELOPMENT.md     # 开发指南 (本文档)
│   └── TEST_REPORT.md     # 测试报告
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── PLAN.md
```

---

## 后端开发

### 添加新模型

1. 在 `backend/app/models/` 下创建模型文件:

```python
# app/models/example.py
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float
from app.core.database import Base, UUIDPk, Timestamped

class ExampleModel(Base, UUIDPk, Timestamped):
    __tablename__ = "exm_example"
    
    name: Mapped[str] = mapped_column(String(100))
    value: Mapped[float] = mapped_column(Float, default=0.0)
```

2. 在 `backend/app/models/__init__.py` 中导入:

```python
from app.models.example import ExampleModel
```

### 添加新 API 路由

1. 在 `backend/app/api/` 下创建路由文件:

```python
# app/api/example.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.example import ExampleModel

router = APIRouter(prefix="/api/example", tags=["示例"])

@router.get("/")
def list_examples(db: Session = Depends(get_db)):
    return db.query(ExampleModel).all()
```

2. 在 `backend/app/main.py` 中注册路由:

```python
from app.api import example
# ...
app.include_router(example.router)
```

### 数据库表前缀规范

| 模块 | 前缀 | 示例 |
|------|------|------|
| 用户 | `usr_` | `usr_user` |
| 简历 | `rsm_` | `rsm_resume` |
| 职位 | `job_` | `job_position` |
| 公司 | `cmp_` | `cmp_company` |
| 面试 | `itv_` | `itv_session` |
| 规划 | `pln_` | `pln_plan` |
| 准备 | `prp_` | `prp_question_bank` |
| 租房 | `rnt_` | `rnt_listing` |
| 系统 | `sys_` | `sys_user_quota` |

---

## 前端开发

### 添加新页面

1. 在 `frontend/src/pages/` 下创建 Vue 组件:

```vue
<!-- pages/example/Example.vue -->
<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/api/client'

const data = ref([])

onMounted(async () => {
  const res = await api.get('/api/example')
  data.value = res
})
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold">示例页面</h1>
    <!-- 内容 -->
  </div>
</template>
```

2. 在 `frontend/src/router/index.js` 中添加路由:

```javascript
{
  path: '/example',
  name: 'example',
  component: () => import('@/pages/example/Example.vue'),
  meta: { title: '示例' }
}
```

### API 调用

```javascript
import { api } from '@/api/client'

// GET 请求
const data = await api.get('/api/example')

// POST 请求
const result = await api.post('/api/example', { name: 'test' })

// PUT 请求
await api.put('/api/example/123', { name: 'updated' })

// DELETE 请求
await api.delete('/api/example/123')
```

### 使用主题变量

```vue
<template>
  <!-- 使用 Tailwind 主题类 -->
  <div class="bg-primary text-white">主题色背景</div>
  <div class="bg-surface text-text">表面色背景</div>
  <div class="border-border">边框色</div>
</template>
```

---

## 数据库设计

### 模型继承体系

```
Base (SQLAlchemy DeclarativeBase)
├── UUIDPk (UUID 主键混入)
├── Timestamped (时间戳混入)
└── 业务模型 (继承 Base + UUIDPk + Timestamped)
```

### 字段类型映射

| Python 类型 | SQLite 类型 | 说明 |
|-------------|------------|------|
| `str` | `TEXT` / `VARCHAR` | 字符串 |
| `int` | `INTEGER` | 整数 |
| `float` | `REAL` | 浮点数 |
| `bool` | `BOOLEAN` | 布尔值 |
| `dict` / `list` | `JSON` (TEXT) | JSON 数据 |
| `datetime` | `DATETIME` | 时间戳 |

---

## API 设计

### RESTful 规范

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/{module}` | 列表查询 |
| GET | `/api/{module}/{id}` | 详情查询 |
| POST | `/api/{module}` | 创建 |
| PUT | `/api/{module}/{id}` | 更新 |
| DELETE | `/api/{module}/{id}` | 删除 |

### 认证方式

```
Authorization: Bearer <token>
```

### 响应格式

```json
// 成功
{
  "id": "xxx",
  "name": "example",
  ...
}

// 错误
{
  "detail": "错误信息"
}
```

---

## 主题系统

跃途支持两套主题一键切换：

### 主题 A — `leap`（专业权威）

```css
--color-primary: #1A56DB;
--color-bg: #F9FAFB;
--color-surface: #FFFFFF;
--color-text: #141B2B;
```

### 主题 B — `flux`（灵动活力）

```css
--color-primary: #7C3AED;
--color-bg: #FAF8FF;
--color-surface: #FFFFFF(80%);
--color-text: #131B2E;
```

### 切换主题

```javascript
import { useThemeStore } from '@/stores/theme'

const theme = useThemeStore()
theme.setTheme('flux')  // 切换到活力主题
theme.setTheme('leap')  // 切换到专业主题
```

---

## 测试指南

### 后端测试

```bash
cd backend

# 安装测试依赖
pip install pytest pytest-cov httpx

# 运行测试
pytest tests/ -v

# 运行测试并生成覆盖率报告
pytest tests/ -v --cov=app --cov-report=html
```

### 前端测试

```bash
cd frontend

# 运行测试
npm run test
```

### API 手动测试

```bash
# 健康检查
curl http://localhost:8000/api/health

# 登录获取 Token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"account":"demo@leappath.app","password":"leappath"}'

# 使用 Token 访问受保护接口
curl http://localhost:8000/api/dashboard \
  -H "Authorization: Bearer <your-token>"
```

---

## 代码规范

### Python

- 遵循 PEP 8
- 使用 type hints
- 函数/类需要 docstring
- 使用 `ruff` 格式化

```bash
# 检查代码风格
ruff check .

# 自动修复
ruff check --fix .

# 格式化
ruff format .
```

### JavaScript/Vue

- 使用 ESLint + Prettier
- Vue 组件使用 `<script setup>`
- 组件文件名 PascalCase
- 使用 Tailwind CSS

```bash
# 检查代码风格
npm run lint

# 自动修复
npm run lint -- --fix
```

### Git 提交规范

```
<type>(<scope>): <description>

类型:
  feat     新功能
  fix      Bug 修复
  docs     文档
  style    格式
  refactor 重构
  test     测试
  chore    构建/工具
  perf     性能优化
```

---

## 常见问题

### Q: 后端启动报错 "module not found"

```bash
# 确保在 backend 目录下
cd backend
# 确保虚拟环境已激活
source .venv/bin/activate
# 重新安装依赖
pip install -r requirements.txt
```

### Q: 前端启动报错 "vite: command not found"

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Q: 数据库表不存在

删除 `backend/leappath.db` 文件，重启后端会自动重建表和种子数据。

### Q: 前端请求后端报 CORS 错误

确保后端已启动，且 `vite.config.js` 中的 proxy 配置正确:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
    },
  },
},
```

### Q: 如何重置种子数据？

```bash
# 删除数据库文件
rm backend/leappath.db

# 重启后端，种子数据会自动重新生成
cd backend && python -m uvicorn app.main:app --reload
```

---

## 📚 相关文档

- [产品需求文档 (PRD)](PRD.md)
- [部署指南](DEPLOYMENT.md)
- [测试报告](TEST_REPORT.md)
- [API 文档](http://localhost:8000/docs) (运行后端后访问)
- [贡献指南](../CONTRIBUTING.md)
- [变更日志](../CHANGELOG.md)
