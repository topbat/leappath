#!/bin/bash
# 跃途 LeapPath — 一键启动脚本
# 使用方法: bash start.sh

set -e

echo "=========================================="
echo "  跃途 LeapPath — 全生命周期 AI 求职助手"
echo "  版本: 1.0.1"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查 Python
echo -e "${BLUE}[1/4]${NC} 检查 Python 环境..."
if ! command -v python &> /dev/null; then
    echo "❌ 未找到 Python，请先安装 Python 3.10+"
    exit 1
fi
PYTHON_VERSION=$(python --version 2>&1)
echo -e "  ✅ ${GREEN}$PYTHON_VERSION${NC}"

# 检查 Node.js
echo -e "${BLUE}[2/4]${NC} 检查 Node.js 环境..."
if ! command -v node &> /dev/null; then
    echo "❌ 未找到 Node.js，请先安装 Node.js 18+"
    exit 1
fi
NODE_VERSION=$(node --version 2>&1)
echo -e "  ✅ ${GREEN}Node.js $NODE_VERSION${NC}"

# 启动后端
echo -e "${BLUE}[3/4]${NC} 启动后端服务..."
cd backend
if [ ! -d ".venv" ]; then
    echo "  创建虚拟环境..."
    python -m venv .venv
fi

# 激活虚拟环境
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

# 安装依赖
echo "  安装 Python 依赖..."
pip install -r requirements.txt -q

# 启动后端（后台运行）
echo "  启动 FastAPI 服务..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# 等待后端启动
echo "  等待后端就绪..."
sleep 3

# 检查后端是否启动成功
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo -e "  ✅ ${GREEN}后端服务已启动${NC} → http://localhost:8000"
else
    echo -e "  ⚠️ ${YELLOW}后端启动中，请稍候...${NC}"
fi

# 启动前端
echo -e "${BLUE}[4/4]${NC} 启动前端服务..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "  安装 npm 依赖..."
    npm install -q
fi

echo "  启动 Vite 开发服务器..."
echo ""
echo "=========================================="
echo -e "  ${GREEN}✅ 跃途 LeapPath 启动成功！${NC}"
echo ""
echo "  🌐 前端应用: http://localhost:5173"
echo "  📡 后端 API: http://localhost:8000"
echo "  📖 API 文档: http://localhost:8000/docs"
echo ""
echo "  📧 登录账号: demo@leappath.app"
echo "  🔑 登录密码: leappath"
echo "=========================================="
echo ""

npm run dev

# 清理
kill $BACKEND_PID 2>/dev/null
