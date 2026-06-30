#!/bin/bash
# 跃途 LeapPath — GitHub 初始化脚本
# 使用方法: bash setup-github.sh <github-username> <repo-name>

set -e

GITHUB_USER=${1:-"your-username"}
REPO_NAME=${2:-"en-job-app"}

echo "=========================================="
echo "  跃途 LeapPath — GitHub 初始化"
echo "  仓库: $GITHUB_USER/$REPO_NAME"
echo "=========================================="

# 检查 gh CLI
if ! command -v gh &> /dev/null; then
    echo "❌ 未找到 GitHub CLI (gh)，请先安装: https://cli.github.com/"
    echo "   或手动在 GitHub 创建仓库后使用 git 命令推送"
    exit 1
fi

# 检查 git
if ! command -v git &> /dev/null; then
    echo "❌ 未找到 Git"
    exit 1
fi

# 初始化 Git 仓库
echo "[1/6] 初始化 Git 仓库..."
if [ ! -d ".git" ]; then
    git init
    echo "  ✅ Git 仓库已初始化"
else
    echo "  ✅ Git 仓库已存在"
fi

# 创建 GitHub 仓库
echo "[2/6] 创建 GitHub 仓库..."
if gh repo view "$GITHUB_USER/$REPO_NAME" &>/dev/null; then
    echo "  ✅ 仓库已存在"
else
    gh repo create "$REPO_NAME" --public --description "跃途 LeapPath — 全生命周期 AI 求职助手" --source=. --remote=origin
    echo "  ✅ 仓库已创建"
fi

# 添加文件
echo "[3/6] 添加文件..."
git add .
echo "  ✅ 文件已暂存"

# 提交
echo "[4/6] 创建提交..."
git commit -m "feat: LeapPath v1.0.1 — 全生命周期 AI 求职助手

- 7 大核心模块: 简历/面试/职位/规划/公司/准备/租房
- 20+ 页面, 双主题切换 (leap/flux)
- FastAPI + Vue 3 全栈架构
- GitHub Actions CI/CD
- 完整文档: README/部署指南/开发指南/测试报告
- MIT 开源许可证" || echo "  ⚠️ 没有新的变更需要提交"

# 推送
echo "[5/6] 推送到 GitHub..."
git branch -M main
git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git" 2>/dev/null || true
git push -u origin main
echo "  ✅ 代码已推送"

# 创建 Release
echo "[6/6] 创建 Release v1.0.1..."
git tag -a v1.0.1 -m "Release v1.0.1

跃途 LeapPath 首个正式版本

功能:
- 7 大核心模块完整实现
- 20+ 页面, 双主题切换
- Mock AI 服务
- 完整文档和测试报告
- GitHub Actions CI/CD"
git push origin v1.0.1
echo "  ✅ Release v1.0.1 已创建"

echo ""
echo "=========================================="
echo "  ✅ GitHub 初始化完成！"
echo ""
echo "  🔗 仓库地址: https://github.com/$GITHUB_USER/$REPO_NAME"
echo "  📋 Release: https://github.com/$GITHUB_USER/$REPO_NAME/releases/tag/v1.0.1"
echo "  📖 README: https://github.com/$GITHUB_USER/$REPO_NAME#readme"
echo "=========================================="
