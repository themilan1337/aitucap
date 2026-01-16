# Multi-Project Auto Deploy Architecture для Ubuntu Server

## Оглавление
1. [Обзор архитектуры](#обзор-архитектуры)
2. [Структура директорий](#структура-директорий)
3. [Схема портов](#схема-портов)
4. [Docker Networking](#docker-networking)
5. [Nginx Reverse Proxy](#nginx-reverse-proxy)
6. [CI/CD Pipeline](#cicd-pipeline)
7. [Управление секретами](#управление-секретами)
8. [Логирование](#логирование)
9. [Zero-Downtime Deployment](#zero-downtime-deployment)
10. [Масштабирование](#масштабирование)

---

## 1. Обзор архитектуры

### Ключевые принципы
- **Изоляция проектов**: Каждый проект в отдельной Docker сети с собственными БД/Redis
- **Centralized Proxy**: Один Nginx управляет всеми входящими соединениями
- **Automated SSL**: Certbot автоматически получает и обновляет сертификаты
- **CI/CD**: GitHub Actions деплоит без простоя
- **Logging**: Структурированное логирование для отладки

### Архитектурная схема
```
Internet
    │
    ▼
┌─────────────────────────────────────────────┐
│ Ubuntu Server (IP: xxx.xxx.xxx.xxx)         │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │ Nginx Reverse Proxy (80/443)         │  │
│  │ + Certbot SSL Manager                │  │
│  └──────────┬───────────────────────────┘  │
│             │                               │
│  ┌──────────┴─────────────┬────────────┐   │
│  │                        │            │   │
│  ▼                        ▼            ▼   │
│ ┌─────────────┐  ┌─────────────┐  ┌──────┐│
│ │ Project 1   │  │ Project 2   │  │ N... ││
│ │             │  │             │  │      ││
│ │ Backend:8001│  │ Backend:8002│  │ :800N││
│ │ Postgres    │  │ Postgres    │  │ ...  ││
│ │ Redis       │  │ Redis       │  │      ││
│ │ (Network 1) │  │ (Network 2) │  │(Net N)│
│ └─────────────┘  └─────────────┘  └──────┘│
└─────────────────────────────────────────────┘
```

---

## 2. Структура директорий

### Организация на сервере
```
/opt/
├── deploy/                          # Скрипты деплоя
│   ├── deploy.sh                    # Главный деплой скрипт
│   ├── health-check.sh              # Проверка здоровья
│   ├── rollback.sh                  # Откат на предыдущую версию
│   └── utils/
│       ├── port-manager.sh          # Управление портами
│       └── backup.sh                # Бэкап БД
│
├── projects/                        # Все проекты
│   ├── muscleup/                    # Текущий проект
│   │   ├── .env                     # Production переменные
│   │   ├── docker-compose.prod.yml  # Production compose
│   │   ├── releases/                # Версии релизов
│   │   │   ├── current -> v1.2.3   # Симлинк на текущую версию
│   │   │   ├── v1.2.3/             # Текущий релиз
│   │   │   │   ├── backend/
│   │   │   │   ├── Dockerfile.prod
│   │   │   │   └── .git/
│   │   │   ├── v1.2.2/             # Предыдущий релиз (для rollback)
│   │   │   └── v1.2.1/             # Старый релиз
│   │   ├── volumes/                # Persistent data
│   │   │   ├── postgres/
│   │   │   ├── redis/
│   │   │   └── models/             # ML модели
│   │   └── logs/                   # Логи приложения
│   │       ├── nginx/
│   │       ├── backend/
│   │       └── archive/
│   │
│   ├── project-2/                  # Другой проект
│   │   └── [аналогичная структура]
│   │
│   └── project-n/                  # N-ый проект
│       └── [аналогичная структура]
│
├── nginx/                          # Nginx конфигурация
│   ├── nginx.conf                  # Главный конфиг
│   ├── conf.d/
│   │   ├── muscleup.conf           # api.muscleup.kz
│   │   ├── project-2.conf          # api.project2.com
│   │   └── ssl-defaults.conf       # SSL настройки
│   ├── ssl/                        # SSL сертификаты
│   │   ├── live/                   # Certbot certs
│   │   └── dhparam.pem             # DH parameters
│   └── logs/
│       ├── access.log
│       └── error.log
│
└── backups/                        # Бэкапы
    ├── databases/
    │   ├── muscleup/
    │   │   ├── daily/
    │   │   └── weekly/
    │   └── project-2/
    └── configs/
```

### Пояснения
- **releases/**: Хранит последние 3 релиза для быстрого отката
- **current symlink**: Позволяет атомарно переключаться между версиями
- **volumes/**: Persistent data переживает пересоздание контейнеров
- **logs/**: Структурированные логи с ротацией

---

## 3. Схема портов

### Принцип распределения портов
```
Проект N → Базовый порт = 8000 + (N * 100)
```

### Таблица портов для MuscleUp (N=1)
| Сервис              | Internal Port | External Port | Описание                    |
|---------------------|---------------|---------------|-----------------------------|
| Backend API         | 8000          | 8001          | FastAPI приложение          |
| PostgreSQL          | 5432          | 5433          | База данных                 |
| Redis               | 6379          | 6380          | Кэш и сессии                |
| WebSocket (если отдельно) | 8000    | 8001          | Через Nginx upgrade         |

### Таблица портов для Project-2 (N=2)
| Сервис              | Internal Port | External Port | Описание                    |
|---------------------|---------------|---------------|-----------------------------|
| Backend API         | 8000          | 8101          | FastAPI приложение          |
| PostgreSQL          | 5432          | 5533          | База данных                 |
| Redis               | 6379          | 6480          | Кэш и сессии                |

### Общие порты (фиксированные)
| Сервис              | Port          | Описание                         |
|---------------------|---------------|----------------------------------|
| Nginx HTTP          | 80            | Редирект на HTTPS                |
| Nginx HTTPS         | 443           | Главный reverse proxy            |

### Port Manager Script
```bash
#!/bin/bash
# /opt/deploy/utils/port-manager.sh

PROJECT_REGISTRY="/opt/projects/.port-registry.json"

# Получить следующий доступный базовый порт
get_next_port() {
    if [ ! -f "$PROJECT_REGISTRY" ]; then
        echo '{"next_project_id": 1, "projects": {}}' > "$PROJECT_REGISTRY"
    fi

    next_id=$(jq -r '.next_project_id' "$PROJECT_REGISTRY")
    base_port=$((8000 + (next_id * 100)))

    echo "$base_port"
}

# Зарегистрировать проект
register_project() {
    local project_name=$1
    local base_port=$2

    jq --arg name "$project_name" \
       --arg port "$base_port" \
       '.projects[$name] = {
           "base_port": ($port | tonumber),
           "backend_port": (($port | tonumber) + 1),
           "postgres_port": (($port | tonumber) + 33),
           "redis_port": (($port | tonumber) + 80)
       } | .next_project_id += 1' \
       "$PROJECT_REGISTRY" > "$PROJECT_REGISTRY.tmp" && \
    mv "$PROJECT_REGISTRY.tmp" "$PROJECT_REGISTRY"
}

# Получить порты проекта
get_project_ports() {
    local project_name=$1
    jq -r ".projects[\"$project_name\"]" "$PROJECT_REGISTRY"
}
```

---

## 4. Docker Networking

### Стратегия сетей

#### Изолированные сети проектов
```yaml
# Каждый проект имеет свою изолированную сеть
networks:
  muscleup-network:
    name: muscleup_internal
    driver: bridge
    internal: false  # Доступ к интернету для API вызовов
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### Production docker-compose.yml
```yaml
# /opt/projects/muscleup/docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: muscleup-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - /opt/projects/muscleup/volumes/postgres:/var/lib/postgresql/data
    networks:
      - muscleup-network
    ports:
      - "127.0.0.1:5433:5432"  # Только localhost
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  redis:
    image: redis:7-alpine
    container_name: muscleup-redis
    restart: unless-stopped
    command: >
      redis-server
      --appendonly yes
      --requirepass ${REDIS_PASSWORD}
      --maxmemory 256mb
      --maxmemory-policy allkeys-lru
    volumes:
      - /opt/projects/muscleup/volumes/redis:/data
    networks:
      - muscleup-network
    ports:
      - "127.0.0.1:6380:6379"  # Только localhost
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  backend:
    build:
      context: ./releases/current/backend
      dockerfile: Dockerfile.prod
    image: muscleup-backend:${VERSION}
    container_name: muscleup-backend
    restart: unless-stopped
    command: >
      sh -c "
        echo 'Running migrations...' &&
        alembic upgrade head &&
        echo 'Starting application...' &&
        uvicorn app.main:app
          --host 0.0.0.0
          --port 8000
          --workers 4
          --loop uvloop
          --log-config logging.conf
      "
    environment:
      # Database
      DATABASE_URL: postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0

      # Security
      SECRET_KEY: ${SECRET_KEY}
      CSRF_SECRET_KEY: ${CSRF_SECRET_KEY}

      # Azure OpenAI
      AZURE_OPENAI_ENDPOINT: ${AZURE_OPENAI_ENDPOINT}
      AZURE_OPENAI_API_KEY: ${AZURE_OPENAI_API_KEY}
      AZURE_OPENAI_DEPLOYMENT: ${AZURE_OPENAI_DEPLOYMENT}
      AZURE_OPENAI_API_VERSION: ${AZURE_OPENAI_API_VERSION}

      # OAuth
      GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID}
      GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET}

      # Production settings
      ENVIRONMENT: production
      COOKIE_DOMAIN: ${COOKIE_DOMAIN}
      COOKIE_SECURE: "true"
      COOKIE_SAMESITE: "none"
      ALLOWED_ORIGINS: ${ALLOWED_ORIGINS}

      # Rate limiting
      RATE_LIMIT_PER_MINUTE: 10
    volumes:
      - /opt/projects/muscleup/volumes/models:/app/models:ro
      - /opt/projects/muscleup/logs/backend:/app/logs
    networks:
      - muscleup-network
    ports:
      - "127.0.0.1:8001:8000"  # Только через Nginx
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
        labels: "service=backend,project=muscleup"
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

networks:
  muscleup-network:
    name: muscleup_internal
    driver: bridge
```

### Production Dockerfile
```dockerfile
# /opt/projects/muscleup/releases/current/backend/Dockerfile.prod
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 1000 appuser

# Copy Python packages from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Create necessary directories
RUN mkdir -p /app/logs /app/models && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 5. Nginx Reverse Proxy

### Главный конфиг
```nginx
# /opt/nginx/nginx.conf
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;

    # Performance
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 100M;  # Для видео загрузки

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml font/truetype font/opentype
               application/vnd.ms-fontobject image/svg+xml;

    # Rate limiting zones
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/s;
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    # Include project configs
    include /opt/nginx/conf.d/*.conf;
}
```

### MuscleUp Project Config
```nginx
# /opt/nginx/conf.d/muscleup.conf

# Upstream для backend (для zero-downtime deployment)
upstream muscleup_backend {
    least_conn;
    server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002 backup;  # Blue-green deployment

    keepalive 32;
}

# HTTP -> HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name api.muscleup.kz;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.muscleup.kz;

    # SSL Configuration
    ssl_certificate /opt/nginx/ssl/live/api.muscleup.kz/fullchain.pem;
    ssl_certificate_key /opt/nginx/ssl/live/api.muscleup.kz/privkey.pem;
    ssl_trusted_certificate /opt/nginx/ssl/live/api.muscleup.kz/chain.pem;

    include /opt/nginx/conf.d/ssl-defaults.conf;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Logging
    access_log /opt/projects/muscleup/logs/nginx/access.log main;
    error_log /opt/projects/muscleup/logs/nginx/error.log warn;

    # Health check endpoint (bypass auth)
    location = /health {
        proxy_pass http://muscleup_backend;
        access_log off;
    }

    # WebSocket upgrade для /api/v1/vision/ws/pose
    location /api/v1/vision/ws/ {
        proxy_pass http://muscleup_backend;

        # WebSocket headers
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Standard headers
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts для long-lived connections
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;

        # Buffering off для real-time
        proxy_buffering off;
    }

    # Auth endpoints (stricter rate limiting)
    location ~ ^/api/v1/auth/(login|register|google) {
        limit_req zone=auth_limit burst=5 nodelay;
        limit_conn addr 5;

        proxy_pass http://muscleup_backend;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # API endpoints
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        limit_conn addr 10;

        proxy_pass http://muscleup_backend;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;  # Для AI обработки
        proxy_read_timeout 300s;

        # Buffering
        proxy_buffering on;
        proxy_buffer_size 4k;
        proxy_buffers 8 4k;
        proxy_busy_buffers_size 8k;
    }

    # Docs (только для staging)
    location ~ ^/(docs|redoc|openapi.json) {
        # Закомментировать для production
        # deny all;

        proxy_pass http://muscleup_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Root
    location / {
        return 200 '{"message": "MuscleUp API", "version": "1.0.0"}';
        add_header Content-Type application/json;
    }
}
```

### SSL Defaults
```nginx
# /opt/nginx/conf.d/ssl-defaults.conf

# SSL Protocols
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
ssl_prefer_server_ciphers off;

# SSL Session
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# DH Parameters
ssl_dhparam /opt/nginx/ssl/dhparam.pem;
```

### Nginx Docker Compose
```yaml
# /opt/nginx/docker-compose.yml
version: '3.8'

services:
  nginx:
    image: nginx:1.25-alpine
    container_name: nginx-proxy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /opt/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - /opt/nginx/conf.d:/opt/nginx/conf.d:ro
      - /opt/nginx/ssl:/opt/nginx/ssl:ro
      - /opt/nginx/logs:/var/log/nginx
      - /var/www/certbot:/var/www/certbot:ro
    networks:
      - proxy-network
    depends_on:
      - certbot
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"

  certbot:
    image: certbot/certbot:latest
    container_name: certbot
    volumes:
      - /opt/nginx/ssl:/etc/letsencrypt
      - /var/www/certbot:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"

networks:
  proxy-network:
    name: proxy_network
    driver: bridge
```

---

## 6. CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'production'
        type: choice
        options:
          - production
          - staging

env:
  PROJECT_NAME: muscleup
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-asyncio pytest-cov

      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
          SECRET_KEY: test-secret-key
          CSRF_SECRET_KEY: test-csrf-key
          AZURE_OPENAI_API_KEY: test-key
          GOOGLE_CLIENT_ID: test-id
          GOOGLE_CLIENT_SECRET: test-secret
        run: |
          pytest tests/ -v --cov=app --cov-report=xml --cov-report=term

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./docker/Dockerfile.prod
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          platforms: linux/amd64

  deploy:
    name: Deploy to Server
    runs-on: ubuntu-latest
    needs: build
    environment: production

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/deploy_key
          chmod 600 ~/.ssh/deploy_key
          ssh-keyscan -H ${{ secrets.SERVER_IP }} >> ~/.ssh/known_hosts

      - name: Get version
        id: version
        run: |
          if [[ $GITHUB_REF == refs/tags/* ]]; then
            echo "version=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
          else
            echo "version=${GITHUB_SHA::8}" >> $GITHUB_OUTPUT
          fi

      - name: Create release directory
        run: |
          ssh -i ~/.ssh/deploy_key ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "
            mkdir -p /opt/projects/${{ env.PROJECT_NAME }}/releases/${{ steps.version.outputs.version }}
          "

      - name: Deploy application
        env:
          SSH_KEY: ~/.ssh/deploy_key
          SSH_USER: ${{ secrets.SSH_USER }}
          SERVER_IP: ${{ secrets.SERVER_IP }}
          VERSION: ${{ steps.version.outputs.version }}
        run: |
          # Sync files
          rsync -avz -e "ssh -i $SSH_KEY" \
            --exclude='.git' \
            --exclude='__pycache__' \
            --exclude='*.pyc' \
            --exclude='.env' \
            ./ $SSH_USER@$SERVER_IP:/opt/projects/${{ env.PROJECT_NAME }}/releases/$VERSION/

          # Deploy
          ssh -i $SSH_KEY $SSH_USER@$SERVER_IP "
            cd /opt/projects/${{ env.PROJECT_NAME }} && \
            export VERSION=$VERSION && \
            bash /opt/deploy/deploy.sh ${{ env.PROJECT_NAME }} $VERSION
          "

      - name: Health check
        run: |
          sleep 10
          ssh -i ~/.ssh/deploy_key ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "
            bash /opt/deploy/health-check.sh ${{ env.PROJECT_NAME }}
          "

      - name: Rollback on failure
        if: failure()
        run: |
          ssh -i ~/.ssh/deploy_key ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "
            bash /opt/deploy/rollback.sh ${{ env.PROJECT_NAME }}
          "

      - name: Cleanup old releases
        if: success()
        run: |
          ssh -i ~/.ssh/deploy_key ${{ secrets.SSH_USER }}@${{ secrets.SERVER_IP }} "
            cd /opt/projects/${{ env.PROJECT_NAME }}/releases && \
            ls -t | tail -n +4 | xargs -r rm -rf
          "

      - name: Notify deployment
        if: always()
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: 'Deployment ${{ job.status }}: ${{ env.PROJECT_NAME }} v${{ steps.version.outputs.version }}'
          webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Deploy Script
```bash
#!/bin/bash
# /opt/deploy/deploy.sh

set -e

PROJECT_NAME=$1
VERSION=$2

if [ -z "$PROJECT_NAME" ] || [ -z "$VERSION" ]; then
    echo "Usage: $0 <project_name> <version>"
    exit 1
fi

PROJECT_DIR="/opt/projects/$PROJECT_NAME"
RELEASE_DIR="$PROJECT_DIR/releases/$VERSION"
CURRENT_LINK="$PROJECT_DIR/releases/current"

echo "========================================="
echo "Deploying $PROJECT_NAME version $VERSION"
echo "========================================="

# 1. Проверка, что релиз существует
if [ ! -d "$RELEASE_DIR" ]; then
    echo "Error: Release directory $RELEASE_DIR does not exist"
    exit 1
fi

# 2. Бэкап текущей версии (для rollback)
if [ -L "$CURRENT_LINK" ]; then
    PREVIOUS_VERSION=$(readlink "$CURRENT_LINK" | xargs basename)
    echo "Current version: $PREVIOUS_VERSION"
    echo "Backing up current version..."
    echo "$PREVIOUS_VERSION" > "$PROJECT_DIR/.previous_version"
fi

# 3. Бэкап базы данных
echo "Creating database backup..."
bash /opt/deploy/utils/backup.sh "$PROJECT_NAME"

# 4. Загрузка переменных окружения
if [ -f "$PROJECT_DIR/.env" ]; then
    set -a
    source "$PROJECT_DIR/.env"
    set +a
else
    echo "Warning: .env file not found"
fi

# 5. Копирование .env в новый релиз
cp "$PROJECT_DIR/.env" "$RELEASE_DIR/.env"

# 6. Создание docker-compose.prod.yml с правильными путями
cat > "$RELEASE_DIR/docker-compose.prod.yml" <<EOF
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: ${PROJECT_NAME}-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: \${POSTGRES_USER}
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
      POSTGRES_DB: \${POSTGRES_DB}
    volumes:
      - $PROJECT_DIR/volumes/postgres:/var/lib/postgresql/data
    networks:
      - ${PROJECT_NAME}-network
    ports:
      - "127.0.0.1:\${POSTGRES_EXTERNAL_PORT}:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U \${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  redis:
    image: redis:7-alpine
    container_name: ${PROJECT_NAME}-redis
    restart: unless-stopped
    command: >
      redis-server
      --appendonly yes
      --requirepass \${REDIS_PASSWORD}
      --maxmemory 256mb
      --maxmemory-policy allkeys-lru
    volumes:
      - $PROJECT_DIR/volumes/redis:/data
    networks:
      - ${PROJECT_NAME}-network
    ports:
      - "127.0.0.1:\${REDIS_EXTERNAL_PORT}:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  backend:
    build:
      context: $RELEASE_DIR
      dockerfile: Dockerfile.prod
    image: ${PROJECT_NAME}-backend:${VERSION}
    container_name: ${PROJECT_NAME}-backend
    restart: unless-stopped
    command: >
      sh -c "
        echo 'Running migrations...' &&
        alembic upgrade head &&
        echo 'Starting application...' &&
        uvicorn app.main:app
          --host 0.0.0.0
          --port 8000
          --workers \${WORKERS:-4}
          --loop uvloop
      "
    env_file:
      - $RELEASE_DIR/.env
    volumes:
      - $PROJECT_DIR/volumes/models:/app/models:ro
      - $PROJECT_DIR/logs/backend:/app/logs
    networks:
      - ${PROJECT_NAME}-network
    ports:
      - "127.0.0.1:\${BACKEND_EXTERNAL_PORT}:8000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "5"
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

networks:
  ${PROJECT_NAME}-network:
    name: ${PROJECT_NAME}_internal
    driver: bridge
EOF

# 7. Blue-Green Deployment
echo "Starting new version on backup port..."

# Временно запускаем на backup порту
export BACKEND_EXTERNAL_PORT=$((BACKEND_EXTERNAL_PORT + 1))

cd "$RELEASE_DIR"
docker-compose -f docker-compose.prod.yml up -d

# 8. Ожидание готовности
echo "Waiting for new version to be ready..."
HEALTH_URL="http://127.0.0.1:$BACKEND_EXTERNAL_PORT/health"
RETRIES=30

for i in $(seq 1 $RETRIES); do
    if curl -f -s "$HEALTH_URL" > /dev/null; then
        echo "New version is healthy!"
        break
    fi

    if [ $i -eq $RETRIES ]; then
        echo "Health check failed after $RETRIES attempts"
        docker-compose -f docker-compose.prod.yml logs --tail=50
        docker-compose -f docker-compose.prod.yml down
        exit 1
    fi

    echo "Attempt $i/$RETRIES: Waiting for health check..."
    sleep 2
done

# 9. Переключение симлинка (атомарная операция)
echo "Switching to new version..."
ln -sfn "$RELEASE_DIR" "$CURRENT_LINK.tmp"
mv -Tf "$CURRENT_LINK.tmp" "$CURRENT_LINK"

# 10. Перезапуск на основном порту
export BACKEND_EXTERNAL_PORT=$((BACKEND_EXTERNAL_PORT - 1))
docker-compose -f docker-compose.prod.yml up -d --force-recreate backend

# Ждем готовности на основном порту
sleep 5
HEALTH_URL="http://127.0.0.1:$BACKEND_EXTERNAL_PORT/health"
for i in $(seq 1 10); do
    if curl -f -s "$HEALTH_URL" > /dev/null; then
        break
    fi
    sleep 2
done

# 11. Остановка старой версии
if [ -n "$PREVIOUS_VERSION" ]; then
    echo "Stopping previous version..."
    cd "$PROJECT_DIR/releases/$PREVIOUS_VERSION"
    docker-compose -f docker-compose.prod.yml down || true
fi

# 12. Обновление Nginx (если нужно)
echo "Reloading Nginx..."
docker exec nginx-proxy nginx -s reload

# 13. Финальная проверка
echo "Final health check..."
if curl -f -s "$HEALTH_URL" > /dev/null; then
    echo "========================================="
    echo "Deployment successful!"
    echo "Version: $VERSION"
    echo "========================================="
else
    echo "Final health check failed, rolling back..."
    bash /opt/deploy/rollback.sh "$PROJECT_NAME"
    exit 1
fi
```

### Health Check Script
```bash
#!/bin/bash
# /opt/deploy/health-check.sh

PROJECT_NAME=$1
PROJECT_DIR="/opt/projects/$PROJECT_NAME"

# Загрузка портов
source "$PROJECT_DIR/.env"

HEALTH_URL="http://127.0.0.1:$BACKEND_EXTERNAL_PORT/health"

echo "Checking health of $PROJECT_NAME..."
echo "URL: $HEALTH_URL"

# HTTP health check
if ! curl -f -s "$HEALTH_URL" > /dev/null; then
    echo "Health check FAILED"
    exit 1
fi

# Docker containers check
if ! docker ps | grep -q "${PROJECT_NAME}-backend"; then
    echo "Backend container not running"
    exit 1
fi

if ! docker ps | grep -q "${PROJECT_NAME}-postgres"; then
    echo "Postgres container not running"
    exit 1
fi

if ! docker ps | grep -q "${PROJECT_NAME}-redis"; then
    echo "Redis container not running"
    exit 1
fi

echo "All health checks PASSED"
exit 0
```

### Rollback Script
```bash
#!/bin/bash
# /opt/deploy/rollback.sh

PROJECT_NAME=$1
PROJECT_DIR="/opt/projects/$PROJECT_NAME"

if [ ! -f "$PROJECT_DIR/.previous_version" ]; then
    echo "No previous version found, cannot rollback"
    exit 1
fi

PREVIOUS_VERSION=$(cat "$PROJECT_DIR/.previous_version")
echo "Rolling back to version: $PREVIOUS_VERSION"

# Используем deploy скрипт для отката
bash /opt/deploy/deploy.sh "$PROJECT_NAME" "$PREVIOUS_VERSION"
```

---

## 7. Управление секретами

### GitHub Secrets (требуются)
```
SSH_PRIVATE_KEY          # SSH ключ для доступа к серверу
SSH_USER                 # SSH пользователь (например, deploy)
SERVER_IP                # IP адрес сервера
SLACK_WEBHOOK           # Webhook для уведомлений (опционально)
```

### .env файл на сервере
```bash
# /opt/projects/muscleup/.env

# Version
VERSION=v1.0.0

# Ports (автоматически назначаются port-manager.sh)
BACKEND_EXTERNAL_PORT=8001
POSTGRES_EXTERNAL_PORT=5433
REDIS_EXTERNAL_PORT=6380

# Workers
WORKERS=4

# Database
POSTGRES_USER=muscleup_prod
POSTGRES_PASSWORD=<сгенерированный_пароль>
POSTGRES_DB=muscleup_production

# Redis
REDIS_PASSWORD=<сгенерированный_пароль>

# Security
SECRET_KEY=<сгенерированный_секрет>
CSRF_SECRET_KEY=<сгенерированный_секрет>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REFRESH_TOKEN_EXPIRE_DAYS_REMEMBER=30

# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://adiletai-openai.openai.azure.com/
AZURE_OPENAI_API_KEY=<ваш_ключ>
AZURE_OPENAI_DEPLOYMENT=gpt-5-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Google OAuth
GOOGLE_CLIENT_ID=<ваш_client_id>
GOOGLE_CLIENT_SECRET=<ваш_client_secret>

# Cookie Settings
COOKIE_DOMAIN=muscleup.kz
COOKIE_SECURE=true
COOKIE_SAMESITE=none

# Rate Limiting
RATE_LIMIT_PER_MINUTE=10

# CORS
ALLOWED_ORIGINS=https://muscleup.kz,https://app.muscleup.kz,muscleup://

# Environment
ENVIRONMENT=production
DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
REDIS_URL=redis://:${REDIS_PASSWORD}@redis:6379/0
```

### Генерация секретов
```bash
#!/bin/bash
# /opt/deploy/utils/generate-secrets.sh

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project_name>"
    exit 1
fi

ENV_FILE="/opt/projects/$PROJECT_NAME/.env"

# Генерация секретов
SECRET_KEY=$(openssl rand -hex 32)
CSRF_SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)

# Получение портов
source /opt/deploy/utils/port-manager.sh
BASE_PORT=$(get_next_port)
BACKEND_PORT=$((BASE_PORT + 1))
POSTGRES_PORT=$((BASE_PORT + 33))
REDIS_PORT=$((BASE_PORT + 80))

# Регистрация проекта
register_project "$PROJECT_NAME" "$BASE_PORT"

# Создание .env файла
cat > "$ENV_FILE" <<EOF
# Auto-generated at $(date)
VERSION=v1.0.0

# Ports
BACKEND_EXTERNAL_PORT=$BACKEND_PORT
POSTGRES_EXTERNAL_PORT=$POSTGRES_PORT
REDIS_EXTERNAL_PORT=$REDIS_PORT

# Workers
WORKERS=4

# Database
POSTGRES_USER=${PROJECT_NAME}_prod
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_DB=${PROJECT_NAME}_production

# Redis
REDIS_PASSWORD=$REDIS_PASSWORD

# Security
SECRET_KEY=$SECRET_KEY
CSRF_SECRET_KEY=$CSRF_SECRET_KEY
ALGORITHM=HS256

# Environment
ENVIRONMENT=production
DATABASE_URL=postgresql+asyncpg://\${POSTGRES_USER}:\${POSTGRES_PASSWORD}@postgres:5432/\${POSTGRES_DB}
REDIS_URL=redis://:\${REDIS_PASSWORD}@redis:6379/0
EOF

chmod 600 "$ENV_FILE"

echo "Secrets generated for $PROJECT_NAME"
echo "Ports: Backend=$BACKEND_PORT, Postgres=$POSTGRES_PORT, Redis=$REDIS_PORT"
echo "IMPORTANT: Add Azure OpenAI and Google OAuth credentials manually to $ENV_FILE"
```

### Безопасное хранение
```bash
# Установка правильных прав
chown -R deploy:deploy /opt/projects/muscleup
chmod 700 /opt/projects/muscleup
chmod 600 /opt/projects/muscleup/.env

# Бэкап секретов (зашифрованный)
gpg --symmetric --cipher-algo AES256 /opt/projects/muscleup/.env
mv /opt/projects/muscleup/.env.gpg /opt/backups/configs/
```

---

## 8. Логирование

### Структура логов

Логи хранятся в структурированном формате для каждого проекта:

```
/opt/projects/muscleup/logs/
├── backend/
│   ├── app.log              # Application logs
│   ├── error.log            # Error logs
│   └── access.log           # Access logs
├── nginx/
│   ├── access.log           # Nginx access logs
│   └── error.log            # Nginx error logs
└── archive/                 # Rotated logs
```

### Docker Logging Configuration

```yaml
# В docker-compose.prod.yml для каждого сервиса
logging:
  driver: "json-file"
  options:
    max-size: "10m"       # Максимальный размер файла лога
    max-file: "5"         # Хранить последние 5 файлов
    labels: "service,project"
```

### Просмотр логов

```bash
# Логи конкретного контейнера
docker logs muscleup_backend -f

# Логи с ограничением по времени
docker logs --since 1h muscleup_backend

# Все логи проекта
tail -f /opt/projects/muscleup/logs/backend/app.log

# Поиск ошибок
grep "ERROR" /opt/projects/muscleup/logs/backend/*.log

# Nginx access лог
tail -f /var/log/nginx/muscleup_access.log
```

### Ротация логов

Настроена автоматическая ротация через Docker и logrotate:

```bash
# /etc/logrotate.d/muscleup
/opt/projects/muscleup/logs/**/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data www-data
    sharedscripts
    postrotate
        docker kill -s USR1 muscleup_backend
    endscript
}
```

---

## 9. Zero-Downtime Deployment

### Стратегия Blue-Green

#### Принцип
1. **Blue** (текущая версия) работает на основном порту
2. **Green** (новая версия) запускается на резервном порту
3. Health check зеленой версии
4. Nginx переключается на зеленую версию
5. Синяя версия останавливается

#### Nginx конфигурация для Blue-Green
```nginx
# Dynamic upstream switching
upstream muscleup_backend {
    least_conn;

    # Primary (Blue)
    server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;

    # Secondary (Green) - активируется во время деплоя
    server 127.0.0.1:8002 backup max_fails=3 fail_timeout=30s;

    keepalive 32;
}
```

#### Обновленный deploy.sh с Blue-Green
```bash
# Фрагмент из deploy.sh

# 7. Blue-Green Deployment
BLUE_PORT=$BACKEND_EXTERNAL_PORT
GREEN_PORT=$((BACKEND_EXTERNAL_PORT + 1))

echo "Blue port: $BLUE_PORT"
echo "Green port: $GREEN_PORT"

# Запуск на green порту
export BACKEND_EXTERNAL_PORT=$GREEN_PORT
docker-compose -f docker-compose.prod.yml up -d

# Health check green
wait_for_health "http://127.0.0.1:$GREEN_PORT/health" 30

# Переключение в Nginx
sed -i "s/server 127.0.0.1:$BLUE_PORT;/server 127.0.0.1:$GREEN_PORT;/" \
    /opt/nginx/conf.d/muscleup.conf
docker exec nginx-proxy nginx -s reload

# Проверка траффика на green
sleep 10

# Остановка blue
docker-compose -f "$PROJECT_DIR/releases/$PREVIOUS_VERSION/docker-compose.prod.yml" down

# Обновление конфига обратно на основной порт
sed -i "s/server 127.0.0.1:$GREEN_PORT;/server 127.0.0.1:$BLUE_PORT;/" \
    /opt/nginx/conf.d/muscleup.conf

# Финальный перезапуск на blue порту с новой версией
export BACKEND_EXTERNAL_PORT=$BLUE_PORT
docker-compose -f docker-compose.prod.yml up -d --force-recreate backend
```

### Rolling Updates для WebSocket
```python
# app/main.py - Graceful shutdown для WebSocket

import signal
import asyncio
from contextlib import asynccontextmanager

shutdown_event = asyncio.Event()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting application...")
    await redis_service.connect()

    # Setup signal handlers
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, lambda: shutdown_event.set())

    yield

    # Shutdown
    logger.info("Shutting down gracefully...")
    shutdown_event.set()

    # Ждем завершения активных WebSocket соединений (макс 30 сек)
    await asyncio.sleep(30)

    await close_db()
    await redis_service.close()
    logger.info("Shutdown complete")
```

---

## 10. Масштабирование

### Добавление нового проекта

#### 1. Автоматический скрипт
```bash
#!/bin/bash
# /opt/deploy/new-project.sh

set -e

PROJECT_NAME=$1
DOMAIN=$2

if [ -z "$PROJECT_NAME" ] || [ -z "$DOMAIN" ]; then
    echo "Usage: $0 <project_name> <domain>"
    echo "Example: $0 fitness-tracker api.fitness-tracker.com"
    exit 1
fi

echo "Creating new project: $PROJECT_NAME"
echo "Domain: $DOMAIN"

# 1. Создание структуры директорий
PROJECT_DIR="/opt/projects/$PROJECT_NAME"
mkdir -p "$PROJECT_DIR"/{releases,volumes/{postgres,redis,models},logs/{nginx,backend}}

# 2. Генерация секретов и портов
bash /opt/deploy/utils/generate-secrets.sh "$PROJECT_NAME"

# 3. Создание Nginx конфига
source "$PROJECT_DIR/.env"

cat > "/opt/nginx/conf.d/${PROJECT_NAME}.conf" <<EOF
# Auto-generated for $PROJECT_NAME

upstream ${PROJECT_NAME}_backend {
    least_conn;
    server 127.0.0.1:$BACKEND_EXTERNAL_PORT max_fails=3 fail_timeout=30s;
    keepalive 32;
}

# HTTP -> HTTPS redirect
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$server_name\$request_uri;
    }
}

# HTTPS server
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $DOMAIN;

    ssl_certificate /opt/nginx/ssl/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /opt/nginx/ssl/live/$DOMAIN/privkey.pem;
    ssl_trusted_certificate /opt/nginx/ssl/live/$DOMAIN/chain.pem;

    include /opt/nginx/conf.d/ssl-defaults.conf;

    access_log /opt/projects/$PROJECT_NAME/logs/nginx/access.log main;
    error_log /opt/projects/$PROJECT_NAME/logs/nginx/error.log warn;

    location /health {
        proxy_pass http://${PROJECT_NAME}_backend;
        access_log off;
    }

    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;

        proxy_pass http://${PROJECT_NAME}_backend;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        proxy_connect_timeout 60s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }

    location / {
        return 200 '{"message": "$PROJECT_NAME API"}';
        add_header Content-Type application/json;
    }
}
EOF

# 4. Получение SSL сертификата
docker exec certbot certbot certonly \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email admin@$DOMAIN \
    --agree-tos \
    --no-eff-email \
    -d $DOMAIN

# 5. Перезагрузка Nginx
docker exec nginx-proxy nginx -s reload

echo "========================================="
echo "Project $PROJECT_NAME created successfully!"
echo "========================================="
echo "Domain: $DOMAIN"
echo "Backend port: $BACKEND_EXTERNAL_PORT"
echo "Postgres port: $POSTGRES_EXTERNAL_PORT"
echo "Redis port: $REDIS_EXTERNAL_PORT"
echo ""
echo "Next steps:"
echo "1. Add Azure OpenAI credentials to $PROJECT_DIR/.env"
echo "2. Add Google OAuth credentials to $PROJECT_DIR/.env"
echo "3. Setup GitHub Actions secrets"
echo "4. Deploy first version"
echo "========================================="
```

#### 2. Использование
```bash
# Создать новый проект
sudo /opt/deploy/new-project.sh fitness-tracker api.fitness-tracker.com

# Деплой
cd /path/to/fitness-tracker/repo
git push origin main  # Автоматический деплой через GitHub Actions
```

### Вертикальное масштабирование

#### Увеличение ресурсов контейнера
```yaml
# docker-compose.prod.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '4'      # Увеличить с 2 до 4
          memory: 4G     # Увеличить с 2G до 4G
        reservations:
          cpus: '2'
          memory: 2G
    environment:
      WORKERS: 8  # Увеличить количество воркеров
```

### Горизонтальное масштабирование

#### Multiple Backend Instances
```yaml
# docker-compose.prod.yml - множественные инстансы
services:
  backend-1:
    <<: *backend-common
    container_name: muscleup-backend-1
    ports:
      - "127.0.0.1:8001:8000"

  backend-2:
    <<: *backend-common
    container_name: muscleup-backend-2
    ports:
      - "127.0.0.1:8002:8000"

  backend-3:
    <<: *backend-common
    container_name: muscleup-backend-3
    ports:
      - "127.0.0.1:8003:8000"
```

#### Nginx load balancing
```nginx
upstream muscleup_backend {
    least_conn;

    server 127.0.0.1:8001 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8002 max_fails=3 fail_timeout=30s;
    server 127.0.0.1:8003 max_fails=3 fail_timeout=30s;

    keepalive 64;
}
```

### Database Scaling

#### Read Replicas
```yaml
services:
  postgres-primary:
    image: postgres:15-alpine
    environment:
      POSTGRES_REPLICATION_MODE: master
    volumes:
      - postgres-primary-data:/var/lib/postgresql/data

  postgres-replica-1:
    image: postgres:15-alpine
    environment:
      POSTGRES_REPLICATION_MODE: slave
      POSTGRES_MASTER_HOST: postgres-primary
    volumes:
      - postgres-replica-1-data:/var/lib/postgresql/data
```

#### Connection Pooling (PgBouncer)
```yaml
services:
  pgbouncer:
    image: edoburu/pgbouncer:latest
    environment:
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      POOL_MODE: transaction
      MAX_CLIENT_CONN: 1000
      DEFAULT_POOL_SIZE: 25
    ports:
      - "127.0.0.1:6432:6432"
```

---

## Резюме

### Ключевые компоненты архитектуры:

1. **Изоляция проектов**
   - Отдельные Docker networks
   - Изолированные БД и Redis
   - Автоматическое распределение портов

2. **Централизованный Reverse Proxy**
   - Nginx с SSL termination
   - Rate limiting
   - WebSocket поддержка

3. **CI/CD**
   - GitHub Actions
   - Automated testing
   - Blue-Green deployment
   - Automated rollback

4. **Security**
   - Encrypted secrets
   - SSL/TLS
   - Minimal container privileges
   - Security headers

5. **High Availability**
   - Health checks
   - Graceful shutdown
   - Zero-downtime deployments
   - Database backups

### Checklist для первого деплоя:

- [ ] Настроить Ubuntu сервер
- [ ] Установить Docker и Docker Compose
- [ ] Создать пользователя `deploy`
- [ ] Настроить SSH ключи
- [ ] Создать структуру `/opt/projects`
- [ ] Установить и настроить Nginx
- [ ] Настроить Certbot для SSL
- [ ] Сгенерировать секреты для проекта
- [ ] Настроить GitHub Secrets
- [ ] Провести тестовый деплой

Эта архитектура позволяет легко масштабироваться от одного до множества проектов, поддерживая при этом высокую доступность и безопасность.
