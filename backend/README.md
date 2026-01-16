# MuscleUp Backend - Production Deployment System

![Production Ready](https://img.shields.io/badge/production-ready-brightgreen)
![Docker](https://img.shields.io/badge/docker-compose-blue)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF)

Полная система автоматического развертывания FastAPI backend с поддержкой множества проектов на одном Ubuntu сервере.

## Особенности

- **Zero-Downtime Deployment** - Blue-Green стратегия развертывания без простоя
- **Multi-Project Support** - Изолированное развертывание множества проектов
- **Automatic SSL** - Let's Encrypt сертификаты с автообновлением
- **CI/CD** - Автоматический деплой через GitHub Actions
- **Security First** - Firewall, Fail2Ban, rate limiting, non-root containers
- **Production Ready** - По лучшим практикам DevOps

## Технологический стек

### Backend
- **Python 3.11** - Язык программирования
- **FastAPI** - Асинхронный веб-фреймворк
- **PostgreSQL 15** - Основная база данных
- **Redis 7** - Кэш и хранилище сессий
- **SQLAlchemy** - Async ORM
- **Alembic** - Миграции БД
- **Azure OpenAI** - AI интеграция
- **RTMPose** - Computer vision для детекции упражнений

### Infrastructure
- **Docker & Docker Compose** - Контейнеризация
- **Nginx** - Reverse proxy с SSL
- **GitHub Actions** - CI/CD pipeline
- **Ubuntu Server** - Production окружение

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/themilan1337/aitucup.git
cd aitucup/backend
```

### 2. Первичная настройка сервера

На Ubuntu сервере запустите:

```bash
sudo bash scripts/deploy/setup-server.sh
```

Этот скрипт установит:
- Docker и Docker Compose
- Nginx с оптимальной конфигурацией
- Certbot для SSL сертификатов
- UFW firewall с правильными правилами
- Fail2Ban для защиты от брутфорса
- Структуру директорий для проектов

### 3. Создание проекта

```bash
sudo /opt/deploy/scripts/new-project.sh muscleup api.muscleup.fitness 8001
```

### 4. Настройка DNS

Добавьте A-запись:
```
api.muscleup.fitness  →  YOUR_SERVER_IP
```

### 5. Получение SSL сертификата

```bash
sudo certbot --nginx -d api.muscleup.fitness
```

### 6. Настройка GitHub Secrets

В GitHub репозитории добавьте secrets (Settings → Secrets → Actions):

```bash
SERVER_HOST=YOUR_SERVER_IP
SERVER_USER=your_username
SERVER_SSH_KEY=<your_private_ssh_key>

POSTGRES_PASSWORD=<strong_password>
SECRET_KEY=<generated_key>
CSRF_SECRET_KEY=<generated_key>

AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_secret
```

Генерация секретов:
```bash
# PostgreSQL пароль
openssl rand -base64 32

# JWT и CSRF ключи
openssl rand -hex 32
```

### 7. Деплой

```bash
git push origin main
```

GitHub Actions автоматически:
1. Запустит тесты
2. Соберет Docker образ
3. Задеплоит на сервер
4. Проверит health checks
5. Переключит трафик на новую версию

## Структура проекта

```
backend/
├── app/                          # Основное приложение
│   ├── main.py                  # Точка входа FastAPI
│   ├── api/v1/                  # API endpoints
│   ├── models/                  # SQLAlchemy модели
│   ├── schemas/                 # Pydantic схемы
│   ├── services/                # Бизнес-логика
│   └── workouts/                # Computer vision
│
├── docker-compose.prod.yml      # Production конфигурация
├── Dockerfile.prod              # Multi-stage production образ
├── .env.production.example      # Шаблон переменных окружения
│
├── .github/workflows/           # CI/CD
│   └── deploy.yml               # Автодеплой pipeline
│
├── nginx/                       # Nginx конфигурация
│   ├── muscleup.conf           # Reverse proxy + SSL
│   └── nginx.conf              # Основные настройки
│
├── scripts/deploy/              # Deployment скрипты
│   ├── setup-server.sh         # Первичная настройка сервера
│   ├── deploy.sh               # Ручной деплой
│   └── rollback.sh             # Откат версии
│
├── DEPLOYMENT.md                # Детальное руководство по деплою
├── PROMPT.md                    # LLM промпт для новых проектов
└── README.md                    # Этот файл
```

## Архитектура

```
Internet
    │
    ▼
┌──────────────────────────────────┐
│ Nginx (80/443)                   │
│ + SSL/TLS + Rate Limiting        │
└─────────┬────────────────────────┘
          │
    ┌─────┴──────┬──────────┐
    ▼            ▼          ▼
┌─────────┐ ┌─────────┐  ┌────┐
│Project 1│ │Project 2│  │ N  │
│:8001    │ │:8101    │  │... │
│Postgres │ │Postgres │  │    │
│Redis    │ │Redis    │  │    │
└─────────┘ └─────────┘  └────┘
```

**Изоляция проектов:**
- Каждый проект в отдельной Docker сети
- Свои базы данных (PostgreSQL, Redis)
- Уникальные порты по формуле: `8000 + (N × 100)`

## Использование

### Локальная разработка

```bash
# Копировать .env
cp .env.example .env

# Запустить с Docker Compose
docker-compose up -d

# Или локально
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Просмотр логов

```bash
# Backend логи
docker logs muscleup_backend -f

# Все логи проекта
tail -f /opt/projects/muscleup/logs/backend/app.log

# Nginx логи
tail -f /var/log/nginx/muscleup_access.log
```

### Ручной деплой

```bash
cd /opt/projects/muscleup
bash /path/to/backend/scripts/deploy/deploy.sh
```

### Откат версии

```bash
bash /path/to/backend/scripts/deploy/rollback.sh
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/oauth` - OAuth вход
- `POST /api/v1/auth/refresh` - Обновить токен
- `POST /api/v1/auth/logout` - Выход

### Workouts
- `POST /api/v1/plans/generate` - Генерация плана тренировок (AI)
- `POST /api/v1/workouts/` - Создать тренировку
- `GET /api/v1/workouts/history` - История тренировок

### Computer Vision
- `WS /api/v1/vision/ws/pose` - WebSocket для real-time детекции поз
- `POST /api/v1/vision/reset-counter` - Сброс счетчика

### Health
- `GET /health` - Health check endpoint

API документация доступна по `/docs` (Swagger UI)

## Безопасность

### Реализованные меры

- ✅ Non-root user в Docker контейнерах
- ✅ SSL/TLS с современными шифрами
- ✅ Security headers (HSTS, CSP, X-Frame-Options)
- ✅ Rate limiting на всех endpoints
- ✅ CSRF защита для cookies
- ✅ JWT токены с коротким TTL
- ✅ Firewall (UFW) настроен
- ✅ Fail2Ban против брутфорса
- ✅ Secrets не в репозитории
- ✅ Read-only volumes где возможно

### Генерация секретов

```bash
# Сильный пароль для БД
openssl rand -base64 32

# JWT secret key
openssl rand -hex 32

# CSRF secret key
openssl rand -hex 32
```

## Мониторинг

### Health Checks

```bash
# Проверка здоровья API
curl https://api.muscleup.fitness/health

# Проверка контейнеров
docker ps | grep muscleup

# Статус всех сервисов
docker-compose -f docker-compose.prod.yml ps
```

### Логи

Логи хранятся в структурированном формате:

```
/opt/projects/muscleup/logs/
├── backend/
│   ├── app.log
│   ├── error.log
│   └── access.log
└── nginx/
    ├── access.log
    └── error.log
```

## Troubleshooting

### Deployment failed

```bash
# Проверить логи GitHub Actions
# Перейти в GitHub → Actions → последний workflow

# Проверить SSH соединение
ssh -i ~/.ssh/deploy_key user@server

# Проверить логи на сервере
docker logs muscleup_backend
```

### Health check failing

```bash
# Проверить статус контейнеров
docker ps -a | grep muscleup

# Проверить логи
docker logs muscleup_backend --tail 100

# Перезапустить
docker restart muscleup_backend
```

### SSL certificate errors

```bash
# Проверить сертификаты
sudo certbot certificates

# Обновить вручную
sudo certbot renew --force-renewal

# Перезагрузить Nginx
sudo systemctl reload nginx
```

### Out of disk space

```bash
# Очистка Docker
docker system prune -a --volumes

# Удаление старых releases
cd /opt/projects/muscleup/releases
ls -t | tail -n +6 | xargs rm -rf

# Очистка логов
find /opt/projects -name "*.log" -mtime +30 -delete
```

## Добавление нового проекта

Эта система поддерживает множество проектов на одном сервере:

### 1. Используйте PROMPT.md

Скопируйте `PROMPT.md` в новый проект и откройте в Cursor AI или ChatGPT:

```bash
cp PROMPT.md /path/to/new-project/
```

AI автоматически сгенерирует все необходимые файлы для вашего нового проекта.

### 2. Создайте проект на сервере

```bash
# Project #2 будет использовать порты 8101, 5533, 6480
sudo /opt/deploy/scripts/new-project.sh myapp api.myapp.com 8101
```

### 3. Настройте DNS и SSL

```bash
# A-запись для домена
# api.myapp.com  →  SERVER_IP

# Получить SSL
sudo certbot --nginx -d api.myapp.com
```

## Производительность

### Оптимизации

- ✅ Multi-stage Docker builds
- ✅ Layer caching
- ✅ Gzip compression в Nginx
- ✅ Connection pooling для БД
- ✅ Redis для кэширования
- ✅ Async/await во всем коде
- ✅ WebSocket keepalive
- ✅ Resource limits в Docker

### Масштабирование

Horizontal scaling (несколько backend инстансов):

```yaml
# В docker-compose.prod.yml
backend:
  deploy:
    replicas: 3
```

Обновите Nginx upstream:
```nginx
upstream muscleup_backend {
    least_conn;
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}
```

## Contributing

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/amazing-feature`)
3. Commit изменения (`git commit -m 'Add amazing feature'`)
4. Push в branch (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## License

This project is licensed under the MIT License.

## Контакты

- GitHub: https://github.com/themilan1337/aitucup
- Issues: https://github.com/themilan1337/aitucup/issues

---

**Made with ❤️ for AITU Cup 2025**

**Generated with Claude Code Multi-Project Deployment System**
