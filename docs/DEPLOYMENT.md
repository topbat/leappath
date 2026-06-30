# 跃途 LeapPath — 部署指南

> **版本**: v1.0.1  
> **更新日期**: 2026-06-30

---

## 📋 目录

- [环境要求](#环境要求)
- [快速部署](#快速部署)
- [生产环境部署](#生产环境部署)
- [Docker 部署](#docker-部署)
- [Nginx 配置](#nginx-配置)
- [环境变量](#环境变量)
- [数据库](#数据库)
- [监控与日志](#监控与日志)
- [常见问题](#常见问题)

---

## 环境要求

| 组件 | 最低版本 | 推荐版本 |
|------|---------|---------|
| Python | 3.10+ | 3.11+ |
| Node.js | 18+ | 20+ |
| npm | 8+ | 10+ |
| SQLite | 3.35+ | 3.40+ |
| Nginx | 1.20+ | 1.24+ (生产环境) |

---

## 快速部署

### 1. 克隆项目

```bash
git clone https://github.com/<your-username>/en-job-app.git
cd en-job-app
```

### 2. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

后端访问地址: `http://localhost:8000`  
API 文档: `http://localhost:8000/docs`

### 3. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
```

前端访问地址: `http://localhost:5173`

### 4. 默认账号

| 项目 | 值 |
|------|-----|
| 邮箱 | `demo@leappath.app` |
| 密码 | `leappath` |

---

## 生产环境部署

### 方案一：Systemd + Nginx

#### 1. 后端服务配置

创建 systemd 服务文件 `/etc/systemd/system/leappath.service`:

```ini
[Unit]
Description=LeapPath Backend API
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/opt/leappath/backend
Environment="PATH=/opt/leappath/backend/.venv/bin"
Environment="LEAPPATH_SECRET_KEY=your-production-secret-key-here"
Environment="LEAPPATH_DEMO_MODE=false"
Environment="LEAPPATH_DATABASE_URL=sqlite:////opt/leappath/data/leappath.db"
ExecStart=/opt/leappath/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

#### 2. 启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable leappath
sudo systemctl start leappath
sudo systemctl status leappath
```

#### 3. Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /opt/leappath/frontend/dist;
        try_files $uri $uri/ /index.html;
        
        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
            expires 30d;
            add_header Cache-Control "public, immutable";
        }
    }

    # API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
    gzip_min_length 1000;
}
```

---

## Docker 部署

### Dockerfile

```dockerfile
# === 构建前端 ===
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# === 构建后端 ===
FROM python:3.11-slim AS backend-build
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .

# === 运行 ===
FROM python:3.11-slim
WORKDIR /app

# 安装依赖
COPY --from=backend-build /app/backend /app/backend
COPY --from=backend-build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# 安装 Nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# 配置
COPY nginx.conf /etc/nginx/sites-available/default

ENV LEAPPATH_SECRET_KEY=change-me-in-production
ENV LEAPPATH_DEMO_MODE=true
ENV LEAPPATH_DATABASE_URL=sqlite:////app/data/leappath.db

EXPOSE 80

# 启动脚本
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

CMD ["/docker-entrypoint.sh"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  leappath:
    build: .
    ports:
      - "80:80"
    volumes:
      - leappath-data:/app/data
    environment:
      - LEAPPATH_SECRET_KEY=${SECRET_KEY:-change-me}
      - LEAPPATH_DEMO_MODE=${DEMO_MODE:-true}
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  leappath-data:
```

### 启动

```bash
# 构建并启动
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

---

## 环境变量

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `LEAPPATH_SECRET_KEY` | JWT 签名密钥 | `leappath-dev-secret-change-me` | ✅ 生产必填 |
| `LEAPPATH_DATABASE_URL` | 数据库连接字符串 | `sqlite:///leappath.db` | ❌ |
| `LEAPPATH_DEMO_MODE` | 演示模式 | `true` | ❌ |
| `LEAPPATH_APP_NAME` | 应用名称 | `跃途 LeapPath API` | ❌ |
| `LEAPPATH_APP_VERSION` | 应用版本 | `1.0.1` | ❌ |

### 生产环境 .env 示例

```env
LEAPPATH_SECRET_KEY=your-super-secret-key-at-least-32-chars
LEAPPATH_DATABASE_URL=sqlite:////opt/leappath/data/leappath.db
LEAPPATH_DEMO_MODE=false
```

---

## 数据库

### SQLite (默认)

开箱即用，适合中小规模部署。数据库文件默认位于 `backend/leappath.db`。

### 备份

```bash
# 手动备份
cp /opt/leappath/data/leappath.db /backup/leappath_$(date +%Y%m%d).db

# 自动备份 (crontab)
0 2 * * * cp /opt/leappath/data/leappath.db /backup/leappath_$(date +\%Y\%m\%d).db
```

### 迁移到 PostgreSQL (可选)

1. 修改 `LEAPPATH_DATABASE_URL`:
   ```
   LEAPPATH_DATABASE_URL=postgresql://user:password@localhost:5432/leappath
   ```

2. 安装驱动:
   ```bash
   pip install psycopg2-binary
   ```

3. 重启服务，自动创建表结构。

---

## 监控与日志

### 健康检查

```bash
curl http://localhost:8000/api/health
# 返回: {"status": "ok"}
```

### 日志

```bash
# Systemd 日志
journalctl -u leappath -f

# Docker 日志
docker-compose logs -f leappath
```

---

## 常见问题

### Q: 端口被占用怎么办？

```bash
# 查找占用端口的进程
lsof -i :8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows

# 修改端口
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Q: 数据库文件权限问题？

```bash
chown -R www-data:www-data /opt/leappath/data/
chmod 755 /opt/leappath/data/
chmod 644 /opt/leappath/data/leappath.db
```

### Q: 前端构建失败？

```bash
# 清除缓存重新安装
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Q: CORS 错误？

检查 `LEAPPATH_CORS_ORIGINS` 配置是否包含前端域名。

---

## 🔐 安全清单

部署前请确认：

- [ ] 已修改 `LEAPPATH_SECRET_KEY` 为强密钥
- [ ] 已设置 `LEAPPATH_DEMO_MODE=false`
- [ ] 已配置 HTTPS (SSL 证书)
- [ ] 已配置防火墙规则
- [ ] 已设置数据库定期备份
- [ ] 已禁用不必要的端口
- [ ] 已配置日志轮转
