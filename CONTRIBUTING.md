# 贡献指南 Contributing Guide

感谢你对 **跃途 LeapPath** 的关注！我们欢迎任何形式的贡献。

---

## 🤝 如何贡献

### 报告 Bug

1. 在 [Issues](../../issues) 中搜索是否已有相同问题
2. 如果没有，创建一个新的 Issue，包含：
   - 清晰的标题和描述
   - 复现步骤
   - 期望行为 vs 实际行为
   - 环境信息（OS、Python版本、Node版本）
   - 截图或错误日志（如有）

### 提交功能建议

1. 在 [Issues](../../issues) 中创建 Feature Request
2. 说明使用场景和期望的解决方案
3. 等待讨论和确认后再开始开发

### 提交代码

#### 1. Fork & Clone

```bash
# Fork 仓库后
git clone https://github.com/<your-username>/en-job-app.git
cd en-job-app
git remote add upstream https://github.com/<original-owner>/en-job-app.git
```

#### 2. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

分支命名规范：
- `feature/xxx` — 新功能
- `fix/xxx` — Bug 修复
- `docs/xxx` — 文档更新
- `refactor/xxx` — 代码重构
- `test/xxx` — 测试相关

#### 3. 开发

```bash
# 后端
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# 前端
cd frontend
npm install
npm run dev
```

#### 4. 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

类型（type）：
- `feat` — 新功能
- `fix` — Bug 修复
- `docs` — 文档
- `style` — 格式（不影响代码运行）
- `refactor` — 重构
- `test` — 测试
- `chore` — 构建/工具
- `perf` — 性能优化

示例：
```
feat(resume): 添加简历 PDF 导出功能
fix(auth): 修复 token 过期后无法自动刷新的问题
docs(readme): 更新部署指南
```

#### 5. 提交 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request：
- 填写清晰的 PR 描述
- 关联相关 Issue（使用 `Closes #123`）
- 确保 CI 通过
- 等待 Code Review

---

## 📋 开发规范

### 代码风格

#### Python (后端)
- 遵循 [PEP 8](https://peps.python.org/pep-0008/)
- 使用 type hints
- 函数和类需要 docstring
- 使用 `ruff` 进行格式化和 lint

#### JavaScript/Vue (前端)
- 使用 ESLint + Prettier
- Vue 组件使用 Composition API (`<script setup>`)
- 组件文件名使用 PascalCase
- 使用 Tailwind CSS 进行样式开发

### 数据库规范

- 表名使用模块前缀：`usr_`, `rsm_`, `job_`, `cmp_`, `itv_`, `pln_`, `prp_`, `rnt_`, `sys_`
- 字段名使用 snake_case
- 所有表必须包含 `id`, `created_at`, `updated_at`

### API 规范

- RESTful 风格
- 路由前缀：`/api/<module>`
- 统一响应格式
- 使用 Pydantic 进行请求验证

---

## 🧪 测试

```bash
# 后端测试
cd backend
pytest tests/ -v --cov=app

# 前端测试
cd frontend
npm run test
```

---

## 📖 文档

- 新功能必须附带文档更新
- API 变更需要更新 `/docs` (FastAPI 自动生成)
- 复杂功能需要在 `docs/` 目录下添加说明文档

---

## 🏷️ Issue 标签

| 标签 | 说明 |
|------|------|
| `bug` | Bug 报告 |
| `enhancement` | 功能增强 |
| `documentation` | 文档相关 |
| `good first issue` | 适合新手 |
| `help wanted` | 需要帮助 |
| `priority: high` | 高优先级 |

---

## 📜 行为准则

- 尊重每一位贡献者
- 建设性地提出反馈
- 专注于对社区最有利的事情
- 对他人表示同理心

---

## ❓ 有问题？

如有任何问题，欢迎在 [Issues](../../issues) 中提问。

再次感谢你的贡献！🎉
