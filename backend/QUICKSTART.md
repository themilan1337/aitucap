# MuscleUp Backend - Quick Start Guide

> Быстрый старт для production deployment на Ubuntu сервере

## Предварительные требования

- Ubuntu Server 20.04+ (рекомендуется 22.04)
- Root или sudo доступ
- Минимум 2GB RAM, 2 CPU cores, 20GB disk
- Домены настроены в DNS:
  - `api.muscleup.fitness` → YOUR_SERVER_IP
  - `app.muscleup.fitness` → YOUR_SERVER_IP
  - `muscleup.fitness` → YOUR_SERVER_IP

## 🚀 3-шаговая установка

### Шаг 1: Настройка сервера

```bash
# Клонировать репозиторий
git clone https://github.com/themilan1337/aitucup.git
cd aitucup/backend

# Установить Docker, Nginx, firewall, etc.
sudo bash scripts/deploy/setup-server.sh
```

Ожидайте ~5-10 минут. Скрипт установит все необходимое.

### Шаг 2: Получить SSL сертификат

```bash
# Автоматическое получение SSL для api.muscleup.fitness
sudo bash scripts/deploy/setup-ssl.sh
```

⚠️ **Важно**: Убедитесь что DNS настроен перед этим шагом!

### Шаг 3: Deploy

```bash
# Локально: настроить GitHub Secrets (см. ниже)
# Затем push в main branch
git push origin main
```

GitHub Actions автоматически задеплоит backend.

---

## ⚙️ GitHub Secrets

Перейдите в **Settings → Secrets and variables → Actions** и добавьте:

### Обязательные secrets

```bash
# SSH доступ к серверу
SERVER_HOST=YOUR_SERVER_IP
SERVER_USER=ubuntu
SERVER_SSH_KEY=<содержимое приватного SSH ключа>

# Database
POSTGRES_PASSWORD=$(openssl rand -base64 32)
DATABASE_URL=postgresql+asyncpg://muscleup_prod:PASSWORD@postgres:5432/muscleup_production

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=$(openssl rand -hex 32)
CSRF_SECRET_KEY=$(openssl rand -hex 32)

# Azure OpenAI (ваши реальные ключи)
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Google OAuth (ваши реальные ключи)
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
```

### Генерация SSH ключа

```bash
# На вашем компьютере
ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/muscleup_deploy -N ""

# Скопировать публичный ключ на сервер
ssh-copy-id -i ~/.ssh/muscleup_deploy.pub ubuntu@YOUR_SERVER_IP

# Приватный ключ для GitHub Secret
cat ~/.ssh/muscleup_deploy
# Скопируйте весь вывод в SERVER_SSH_KEY
```

---

## 📝 Создание .env.production на сервере

```bash
# На сервере
sudo nano /opt/projects/muscleup/.env.production
```

Вставьте:

```bash
# Database
POSTGRES_USER=muscleup_prod
POSTGRES_PASSWORD=<сильный пароль>
POSTGRES_DB=muscleup_production
DATABASE_URL=postgresql+asyncpg://muscleup_prod:<PASSWORD>@postgres:5432/muscleup_production

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=<openssl rand -hex 32>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CSRF
CSRF_SECRET_KEY=<openssl rand -hex 32>
CSRF_TOKEN_EXPIRE_MINUTES=60

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Google OAuth
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_secret

# Cookies & CORS
COOKIE_DOMAIN=api.muscleup.fitness
COOKIE_SECURE=true
COOKIE_SAMESITE=lax
ALLOWED_ORIGINS=https://muscleup.fitness,https://www.muscleup.fitness,https://app.muscleup.fitness

# Application
ENVIRONMENT=production
LOG_LEVEL=info
RATE_LIMIT_PER_MINUTE=10
```

Защитите файл:
```bash
sudo chmod 600 /opt/projects/muscleup/.env.production
```

---

## ✅ Проверка

### 1. Проверить DNS

```bash
nslookup api.muscleup.fitness
# Должен вернуть ваш SERVER_IP
```

### 2. Проверить SSL

```bash
curl -I https://api.muscleup.fitness/health
# Должен вернуть 200 OK
```

### 3. Проверить API

```bash
curl https://api.muscleup.fitness/health
```

Ожидаемый ответ:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected",
  "redis": "connected"
}
```

### 4. Проверить Docker контейнеры

```bash
docker ps | grep muscleup
```

Должны работать 3 контейнера:
- muscleup_backend
- muscleup_postgres
- muscleup_redis

---

## 🔧 Полезные команды

### Логи

```bash
# Backend логи
docker logs muscleup_backend -f

# Все логи
docker-compose -f /opt/projects/muscleup/current/docker-compose.prod.yml logs -f

# Nginx логи
tail -f /var/log/nginx/muscleup_access.log
tail -f /var/log/nginx/muscleup_error.log
```

### Управление

```bash
# Перезапуск backend
docker restart muscleup_backend

# Перезапуск всех сервисов
cd /opt/projects/muscleup/current
docker-compose -f docker-compose.prod.yml restart

# Остановить всё
docker-compose -f docker-compose.prod.yml down

# Запустить всё
docker-compose -f docker-compose.prod.yml up -d
```

### SSL

```bash
# Проверить сертификат
sudo certbot certificates

# Обновить вручную
sudo certbot renew --force-renewal

# Тест авто-обновления
sudo certbot renew --dry-run
```

### Deployment

```bash
# Ручной deploy
cd /opt/projects/muscleup
sudo bash /path/to/backend/scripts/deploy/deploy.sh

# Rollback к предыдущей версии
sudo bash /path/to/backend/scripts/deploy/rollback.sh
```

---

## 🐛 Troubleshooting

### SSL не работает

1. Проверить DNS: `nslookup api.muscleup.fitness`
2. Проверить firewall: `sudo ufw status` (порты 80, 443 должны быть открыты)
3. Проверить Nginx: `sudo nginx -t`
4. Логи Certbot: `sudo tail -f /var/log/letsencrypt/letsencrypt.log`
5. Запустить setup-ssl.sh заново

### Backend не запускается

1. Проверить логи: `docker logs muscleup_backend`
2. Проверить .env.production существует и правильный
3. Проверить PostgreSQL: `docker logs muscleup_postgres`
4. Проверить Redis: `docker logs muscleup_redis`
5. Попробовать перезапуск: `docker-compose restart`

### GitHub Actions failed

1. Проверить все secrets настроены
2. Проверить SSH ключ работает: `ssh -i ~/.ssh/muscleup_deploy ubuntu@SERVER_IP`
3. Проверить логи в GitHub Actions tab
4. Проверить .env.production на сервере

### CORS ошибки

1. Проверить ALLOWED_ORIGINS в .env.production
2. Перезапустить backend: `docker restart muscleup_backend`
3. Проверить Nginx конфигурацию
4. Проверить frontend использует правильный API URL

---

## 📚 Дополнительная документация

- **DEPLOYMENT.md** - Детальное руководство по deployment
- **DOMAINS.md** - Информация о доменах и SSL
- **README.md** - Полная документация проекта
- **UPDATES_SUMMARY.md** - Что было обновлено

---

## 🆘 Поддержка

- **GitHub Issues**: https://github.com/themilan1337/aitucup/issues
- **Email**: admin@muscleup.fitness

---

**Среднее время установки**: ~15 минут
**Сложность**: Средняя
**Статус**: Production Ready ✅
