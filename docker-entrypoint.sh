#!/bin/bash
set -e

echo "=========================================="
echo "  跃途 LeapPath — Docker 启动"
echo "=========================================="

# 创建数据目录
mkdir -p /app/data

# 启动后端（后台）
echo "启动后端服务..."
cd /app/backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2 &
BACKEND_PID=$!

# 等待后端启动
echo "等待后端就绪..."
for i in $(seq 1 30); do
    if curl -s http://127.0.0.1:8000/api/health > /dev/null 2>&1; then
        echo "后端服务已就绪"
        break
    fi
    sleep 1
done

# 启动 Nginx
echo "启动 Nginx..."
nginx -g 'daemon off;' &
NGINX_PID=$!

echo "=========================================="
echo "  ✅ 跃途 LeapPath 启动成功！"
echo "  🌐 访问地址: http://localhost"
echo "  📖 API 文档: http://localhost/docs"
echo "  📧 账号: demo@leappath.app"
echo "  🔑 密码: leappath"
echo "=========================================="

# 等待子进程
wait -n
exit $?
