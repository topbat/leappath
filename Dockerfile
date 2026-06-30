# === 构建前端 ===
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# === 运行 ===
FROM python:3.11-slim
WORKDIR /app

# 系统依赖
RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx curl && \
    rm -rf /var/lib/apt/lists/*

# 后端依赖
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# 复制源码
COPY backend/ ./backend/
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Nginx 配置
COPY nginx.conf /etc/nginx/sites-available/default

# 环境变量
ENV LEAPPATH_SECRET_KEY=change-me-in-production
ENV LEAPPATH_DEMO_MODE=true
ENV LEAPPATH_DATABASE_URL=sqlite:////app/data/leappath.db
ENV PYTHONPATH=/app/backend

# 数据目录
RUN mkdir -p /app/data

# 启动脚本
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

CMD ["/docker-entrypoint.sh"]
