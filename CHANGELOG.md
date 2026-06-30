# Changelog

跃途 LeapPath 所有重要变更均记录于此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [1.0.1] - 2026-06-30

### Added
- 完整的 GitHub README 文档，含功能截图、开源协议、贡献指引
- MIT 开源许可证
- GitHub Actions CI/CD 流水线（push触发、workflow_dispatch网页触发、脚本触发）
- 完整测试报告（安全测试、性能测试、功能测试）
- 部署指南 (`docs/DEPLOYMENT.md`)
- 开发指南 (`docs/DEVELOPMENT.md`)
- `.gitignore` 文件
- `CHANGELOG.md` 变更记录文件

### Changed
- 版本号从 1.0.0 升级至 1.0.1

### Security
- 安全测试覆盖：认证机制、CORS配置、SQL注入防护、XSS防护、密码存储

---

## [1.0.0] - 2026-06-25

### Added
- **品牌系统**：跃途 LeapPath 命名、LOGO（SVG）、双主题色彩方案
- **后端基座**：FastAPI + SQLAlchemy + SQLite，统一配置、数据库引擎、安全模块
- **数据模型**：7大业务模块（用户/简历/职位/公司/面试/规划/准备/租房）共15+张数据表
- **API 路由**：认证、简历、面试、职位、公司、规划、准备、租房、仪表盘共9组路由
- **Mock AI 服务**：模拟AI简历润色、面试对话、评分功能
- **种子数据**：演示用户、简历、公司（腾讯/字节/美团/招行）、职位、投递、题库、Offer、房源
- **前端基座**：Vue 3 + Vite + Pinia + Tailwind CSS，双主题切换（leap/flux）
- **前端页面**：20个页面覆盖全部7大模块
  - 工作台仪表盘
  - 简历中心（列表/编辑/优化/评分）
  - 模拟面试（配置/会话/报告/历史）
  - 职位匹配（列表/详情/投递追踪）
  - 求职规划（时间线/任务/学习路径）
  - 公司画像（列表/详情/对比）
  - 求职准备（题库/Offer评估）
  - 租房选址（地图/筛选）
  - 个人中心
- **组件库**：通用组件（Icon/Logo/ThemeToggle/EmptyState/AiThinking/PageHeader）
- **图表组件**：ScoreRing/RadarChart/ProgressBar
- **布局系统**：AppShell 响应式布局，侧边栏导航
- **API 客户端**：封装 fetch，自动携带 token，演示模式支持
- **用户状态管理**：Pinia store，登录/注册/登出

---

## [Unreleased]

### Planned
- 微信小程序端
- 真实 AI 服务接入
- 职位数据自动聚合
- 地图 SDK 集成（高德/腾讯地图）
- 简历 PDF 导出
- 语音面试功能
