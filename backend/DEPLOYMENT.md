# Production Deployment Guide

Полное руководство по развертыванию MuscleUp Backend на production сервере с поддержкой множества проектов.

## Содержание

1. [Обзор архитектуры](#обзор-архитектуры)
2. [Первичная настройка сервера](#первичная-настройка-сервера)
3. [Настройка GitHub Actions](#настройка-github-actions)
4. [Деплой проекта](#деплой-проекта)
5. [Управление и обслуживание](#управление-и-обслуживание)
6. [Troubleshooting](#troubleshooting)

---

## Обзор архитектуры

### Структура сервера

```
Ubuntu Server
├── /opt/projects/                    # Все проекты
│   └── muscleup/                     # Проект MuscleUp
│       ├── current -> releases/XXX   # Симлинк на текущий релиз
│       ├── releases/                 # Все релизы
│       │   ├── 20260116_120000/     # Релиз по timestamp
│       │   └── abc123def/           # Релиз по git SHA
│       └── shared/                   # Общие данные
│           ├── logs/
│           └── backups/
│
├── /opt/deploy/                      # Deployment инфраструктура
│   ├── scripts/                      # Скрипты для деплоя
│   └── configs/                      # Общие конфигурации
│
└── /etc/nginx/                       # Nginx конфигурация
    ├── sites-available/
    │   └── muscleup.conf
    └── sites-enabled/
        └── muscleup.conf -> ../sites-available/muscleup.conf
```

### Технологии

- **Docker & Docker Compose**: Контейнеризация и оркестрация
- **Nginx**: Reverse proxy, SSL termination, rate limiting
- **Let's Encrypt**: Автоматические SSL сертификаты
- **GitHub Actions**: CI/CD pipeline
- **Blue-Green Deployment**: Zero-downtime обновления

### Порты

Формула распределения портов: `Base Port = 8000 + (Project_Number × 100)`

**MuscleUp (Project #1)**:
- Backend: `8001`
- PostgreSQL: `5433`
- Redis: `6380`

---

## Первичная настройка сервера

### Шаг 1: Подготовка сервера

Требования:
- Ubuntu 20.04+ (рекомендуется 22.04)
- Минимум 2GB RAM, 2 CPU cores
- 20GB свободного места
- Доступ по SSH с правами sudo

### Шаг 2: Запуск setup скрипта

```bash
# Склонировать репозиторий на сервер
git clone https://github.com/themilan1337/aitucup.git
cd aitucup/backend

# Запустить установку
sudo bash scripts/deploy/setup-server.sh
```

**Что устанавливает скрипт:**
1. Обновление системных пакетов
2. Docker и Docker Compose
3. Nginx
4. UFW (Firewall)
5. Fail2Ban (защита от брутфорса)
6. Certbot (Let's Encrypt)
7. Структура директорий для проектов

### Шаг 3: Создание проекта на сервере

```bash
sudo /opt/deploy/scripts/new-project.sh muscleup api.muscleup.fitness 8001
```

**Параметры:**
- `muscleup` - имя проекта
- `api.muscleup.fitness` - домен
- `8001` - базовый порт

### Шаг 4: Настройка DNS

Добавьте A-запись для вашего домена:
```
api.muscleup.fitness.  A  YOUR_SERVER_IP
```

### Шаг 5: Получение SSL сертификата

```bash
# После настройки DNS (подождите распространения DNS ~5-10 минут)
sudo certbot --nginx -d api.muscleup.fitness

# Выберите опции:
# 1. Email для уведомлений
# 2. Agree to Terms of Service
# 3. Redirect HTTP to HTTPS (рекомендуется)
```

Автообновление сертификатов настроено автоматически через cron.

---

## Настройка GitHub Actions

### Шаг 1: Генерация SSH ключа для деплоя

На вашем компьютере:

```bash
# Генерация SSH ключа без пароля
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/muscleup_deploy -N ""

# Скопировать публичный ключ на сервер
ssh-copy-id -i ~/.ssh/muscleup_deploy.pub user@YOUR_SERVER_IP

# Вывести приватный ключ (для GitHub Secrets)
cat ~/.ssh/muscleup_deploy
```

### Шаг 2: Настройка GitHub Secrets

Перейдите в GitHub: **Repository → Settings → Secrets and variables → Actions**

Добавьте следующие secrets:

#### Обязательные secrets:

```bash
SERVER_HOST=YOUR_SERVER_IP
SERVER_USER=your_ssh_username
SERVER_SSH_KEY=<содержимое приватного ключа>
SERVER_PORT=22

# Database
POSTGRES_USER=muscleup_prod
POSTGRES_PASSWORD=<генерируйте сильный пароль>
POSTGRES_DB=muscleup_production
DATABASE_URL=postgresql+asyncpg://muscleup_prod:<PASSWORD>@postgres:5432/muscleup_production

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=<генерируйте: openssl rand -hex 32>
CSRF_SECRET_KEY=<генерируйте: openssl rand -hex 32>

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Docker Hub (опционально)
DOCKER_USERNAME=your_dockerhub_username
DOCKER_PASSWORD=your_dockerhub_password
```

#### Генерация безопасных паролей:

```bash
# Сложный пароль для PostgreSQL
openssl rand -base64 32

# Secret key для JWT
openssl rand -hex 32

# CSRF secret key
openssl rand -hex 32
```

### Шаг 3: Создание .env.production на сервере

```bash
# На сервере создайте файл
sudo nano /opt/projects/muscleup/.env.production
```

Вставьте (заполните реальными значениями):

```bash
# Database
POSTGRES_USER=muscleup_prod
POSTGRES_PASSWORD=YOUR_STRONG_PASSWORD
POSTGRES_DB=muscleup_production
DATABASE_URL=postgresql+asyncpg://muscleup_prod:YOUR_STRONG_PASSWORD@postgres:5432/muscleup_production

# Redis
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=YOUR_SECRET_KEY_FROM_OPENSSL
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CSRF
CSRF_SECRET_KEY=YOUR_CSRF_SECRET_KEY
CSRF_TOKEN_EXPIRE_MINUTES=60

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Google OAuth
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret

# Cookies & CORS
COOKIE_DOMAIN=api.muscleup.fitness
COOKIE_SECURE=true
COOKIE_SAMESITE=lax
ALLOWED_ORIGINS=https://muscleup.fitness,https://www.muscleup.fitness

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

## Деплой проекта

### Автоматический деплой через GitHub Actions

После настройки secrets, каждый push в `main` ветку автоматически запускает деплой:

```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

**Этапы CI/CD pipeline:**

1. **Test** (2-3 мин):
   - Запуск линтеров (Black, Ruff)
   - Запуск тестов с coverage
   - Загрузка отчетов в Codecov

2. **Build** (3-5 мин):
   - Сборка Docker образа
   - Оптимизация слоев
   - Экспорт артефакта

3. **Deploy** (2-4 мин):
   - Копирование файлов на сервер
   - Загрузка Docker образа
   - Blue-Green deployment
   - Health checks
   - Переключение трафика

**Общее время:** ~7-12 минут

### Ручной деплой (для emergencies)

Если GitHub Actions недоступен:

```bash
# На сервере
cd /opt/projects/muscleup
sudo bash /path/to/backend/scripts/deploy/deploy.sh
```

### Rollback (откат)

Если что-то пошло не так:

```bash
# Автоматический откат к предыдущей версии
sudo bash /path/to/backend/scripts/deploy/rollback.sh
```

Или через GitHub Actions:
1. Go to **Actions** tab
2. Select **Deploy to Production** workflow
3. Click **Run workflow**
4. Select **rollback** job

---

## Управление и обслуживание

### Проверка статуса

```bash
# Статус всех контейнеров
docker ps -a | grep muscleup

# Логи backend
docker logs muscleup_backend -f

# Логи PostgreSQL
docker logs muscleup_postgres -f

# Логи Redis
docker logs muscleup_redis -f

# Health check
curl https://api.muscleup.fitness/health
```

### Управление контейнерами

```bash
# Перезапуск backend
docker restart muscleup_backend

# Остановка всех сервисов
cd /opt/projects/muscleup/current
docker-compose -f docker-compose.prod.yml down

# Запуск всех сервисов
docker-compose -f docker-compose.prod.yml up -d

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f
```

### Backup базы данных

```bash
# Создание backup
docker exec muscleup_postgres pg_dump -U muscleup_prod muscleup_production > backup_$(date +%Y%m%d).sql

# Восстановление
cat backup_20260116.sql | docker exec -i muscleup_postgres psql -U muscleup_prod muscleup_production
```

### Обновление Nginx конфигурации

```bash
# Редактировать конфигурацию
sudo nano /etc/nginx/sites-available/muscleup.conf

# Проверить синтаксис
sudo nginx -t

# Перезагрузить Nginx
sudo systemctl reload nginx
```

### Просмотр использования ресурсов

```bash
# Использование контейнерами
docker stats

# Дисковое пространство
df -h
docker system df

# Очистка неиспользуемых образов
docker system prune -a
```

---

## Troubleshooting

### Проблема: Deployment failed в GitHub Actions

**Решение:**
1. Проверьте логи в Actions tab
2. Убедитесь, что все secrets настроены
3. Проверьте SSH соединение:
   ```bash
   ssh -i ~/.ssh/muscleup_deploy user@YOUR_SERVER_IP
   ```

### Проблема: Health check failing

**Решение:**
```bash
# Проверьте логи backend
docker logs muscleup_backend

# Проверьте доступность БД
docker exec muscleup_postgres pg_isready -U muscleup_prod

# Проверьте доступность Redis
docker exec muscleup_redis redis-cli ping

# Попробуйте перезапустить
docker restart muscleup_backend
```

### Проблема: SSL certificate errors

**Решение:**
```bash
# Проверьте статус сертификата
sudo certbot certificates

# Обновите сертификат вручную
sudo certbot renew --force-renewal

# Перезагрузите Nginx
sudo systemctl reload nginx
```

### Проблема: Port already in use

**Решение:**
```bash
# Найдите процесс на порту
sudo netstat -tlnp | grep 8001

# Остановите старые контейнеры
docker ps -a | grep muscleup
docker stop <container_id>
docker rm <container_id>
```

### Проблема: Out of disk space

**Решение:**
```bash
# Очистка Docker
docker system prune -a --volumes

# Удаление старых релизов (оставить последние 5)
cd /opt/projects/muscleup/releases
ls -t | tail -n +6 | xargs rm -rf

# Очистка логов
sudo find /opt/projects/muscleup -name "*.log" -mtime +30 -delete
```

### Проблема: Database migration errors

**Решение:**
```bash
# Войдите в контейнер
docker exec -it muscleup_backend bash

# Запустите миграции вручную
alembic upgrade head

# Или откатитесь
alembic downgrade -1
```

### Проблема: 502 Bad Gateway

**Причины и решения:**

1. **Backend не запущен:**
   ```bash
   docker ps | grep muscleup_backend
   docker start muscleup_backend
   ```

2. **Backend не прошел health check:**
   ```bash
   docker logs muscleup_backend
   # Исправьте ошибки и перезапустите
   ```

3. **Неправильная Nginx конфигурация:**
   ```bash
   sudo nginx -t
   # Исправьте ошибки в /etc/nginx/sites-available/muscleup.conf
   ```

### Проблема: CORS errors

**Решение:**
```bash
# Проверьте ALLOWED_ORIGINS в .env.production
sudo nano /opt/projects/muscleup/.env.production

# Должно быть:
ALLOWED_ORIGINS=https://muscleup.fitness,https://www.muscleup.fitness

# Перезапустите backend
docker restart muscleup_backend
```

---

## Добавление нового проекта на сервер

Сервер спроектирован для множества проектов. Чтобы добавить новый:

### 1. Выберите номер проекта и порты

```
Project #2:
- Base port: 8100
- Backend: 8101
- PostgreSQL: 5533
- Redis: 6480
```

### 2. Создайте проект

```bash
sudo /opt/deploy/scripts/new-project.sh myapp api.myapp.com 8101
```

### 3. Настройте DNS и SSL

```bash
# Добавьте A-запись для api.myapp.com
sudo certbot --nginx -d api.myapp.com
```

### 4. Используйте PROMPT.md

В новом проекте скопируйте `PROMPT.md` и используйте его с AI ассистентом (Claude, ChatGPT, Cursor):

```bash
cp /opt/projects/muscleup/PROMPT.md /path/to/new-project/
```

Откройте PROMPT.md в Cursor AI или другом AI ассистенте - он автоматически сгенерирует все необходимые конфигурационные файлы для нового проекта.

---

## Безопасность

### Чеклист безопасности

- [ ] Firewall настроен (UFW)
- [ ] Fail2Ban активен
- [ ] SSL сертификаты установлены
- [ ] Secrets не в git репозитории
- [ ] .env.production с правами 600
- [ ] Non-root user в Docker контейнерах
- [ ] Rate limiting настроен в Nginx
- [ ] Регулярные backups БД
- [ ] Обновления системы автоматические

### Обновление безопасности

```bash
# Обновление системных пакетов
sudo apt update && sudo apt upgrade -y

# Обновление Docker образов
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

---

## Полезные команды

### Docker

```bash
# Просмотр всех контейнеров
docker ps -a

# Просмотр образов
docker images

# Очистка
docker system prune -a

# Exec в контейнер
docker exec -it muscleup_backend bash

# Копирование файлов
docker cp muscleup_backend:/app/logs/app.log ./
```

### Nginx

```bash
# Проверка конфигурации
sudo nginx -t

# Перезагрузка
sudo systemctl reload nginx

# Просмотр логов
sudo tail -f /var/log/nginx/muscleup_access.log
sudo tail -f /var/log/nginx/muscleup_error.log
```

### PostgreSQL

```bash
# Подключение к БД
docker exec -it muscleup_postgres psql -U muscleup_prod muscleup_production

# Backup
docker exec muscleup_postgres pg_dump -U muscleup_prod muscleup_production > backup.sql

# Restore
cat backup.sql | docker exec -i muscleup_postgres psql -U muscleup_prod muscleup_production
```

---

## Контакты и поддержка

- GitHub: https://github.com/themilan1337/aitucup
- Issues: https://github.com/themilan1337/aitucup/issues

---

**Дата создания:** 2026-01-16
**Версия:** 1.0
**Статус:** Production Ready
