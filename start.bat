@echo off
REM 跃途 LeapPath — 一键启动脚本 (Windows)
REM 使用方法: 双击 start.bat 或在命令行运行

echo ==========================================
echo   跃途 LeapPath — 全生命周期 AI 求职助手
echo   版本: 1.0.1
echo ==========================================
echo.

REM 检查 Python
echo [1/4] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VER=%%i
echo   ✅ %PYTHON_VER%

REM 检查 Node.js
echo [2/4] 检查 Node.js 环境...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VER=%%i
echo   ✅ Node.js %NODE_VER%

REM 启动后端
echo [3/4] 启动后端服务...
cd backend
if not exist ".venv" (
    echo   创建虚拟环境...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
echo   安装 Python 依赖...
pip install -r requirements.txt -q
echo   启动 FastAPI 服务...
start "LeapPath Backend" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
cd ..

REM 等待后端启动
echo   等待后端就绪...
timeout /t 3 /nobreak >nul

echo   ✅ 后端服务已启动 → http://localhost:8000

REM 启动前端
echo [4/4] 启动前端服务...
cd frontend
if not exist "node_modules" (
    echo   安装 npm 依赖...
    call npm install -q
)

echo.
echo ==========================================
echo   ✅ 跃途 LeapPath 启动成功！
echo.
echo   🌐 前端应用: http://localhost:5173
echo   📡 后端 API: http://localhost:8000
echo   📖 API 文档: http://localhost:8000/docs
echo.
echo   📧 登录账号: demo@leappath.app
echo   🔑 登录密码: leappath
echo ==========================================
echo.

call npm run dev
