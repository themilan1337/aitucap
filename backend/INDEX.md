# MuscleUp Backend - Documentation Index

> Навигация по всей документации проекта

## 🚀 Быстрый старт

**Начните здесь:**
1. **[QUICKSTART.md](QUICKSTART.md)** - Быстрая установка за 3 шага (8K)
2. **[PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)** - Checklist для deployment (10K)

## 📚 Основная документация

### Для разработчиков
- **[README.md](README.md)** - Главная документация проекта (12K)
  - Обзор проекта
  - Технологический стек
  - API endpoints
  - Локальная разработка

### Для DevOps
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Детальное руководство по deployment (17K)
  - Первичная настройка сервера
  - GitHub Actions setup
  - Управление и обслуживание
  - Troubleshooting

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Техническая архитектура (51K)
  - Структура проектов на сервере
  - Docker networking
  - Nginx конфигурация
  - Blue-Green deployment

## 🌐 Domains & SSL

- **[DOMAINS.md](DOMAINS.md)** - Всё о доменах и SSL (5K)
  - DNS конфигурация
  - SSL setup (автоматический)
  - CORS настройки
  - Troubleshooting

## 🐛 Troubleshooting

- **[DOCKER_PERMISSIONS.md](DOCKER_PERMISSIONS.md)** - Решение проблем с Docker permissions
  - "permission denied" ошибки
  - Как правильно перелогиниться
  - Альтернативные решения
  - Rootless Docker

## 📝 Updates & Changes

- **[UPDATES_SUMMARY.md](UPDATES_SUMMARY.md)** - Последние обновления (6K)
  - Что изменилось
  - Новые production домены
  - Автоматический SSL

- **[SETUP_SUMMARY.md](SETUP_SUMMARY.md)** - Краткое резюме системы (3K)
  - Обзор архитектуры
  - Созданные файлы
  - Quick start

## 🔧 Для AI-ассистентов

- **[PROMPT.md](PROMPT.md)** - LLM промпт для новых проектов (12K)
  - Используйте в Cursor AI или ChatGPT
  - Автоматическая генерация deployment файлов
  - Совместимость с существующей инфраструктурой

## 📋 Production Info

### Домены
- **Landing**: https://muscleup.fitness
- **Dashboard**: https://app.muscleup.fitness
- **API**: https://api.muscleup.fitness

### SSL
- **Domain**: api.muscleup.fitness
- **Email**: admin@muscleup.fitness
- **Auto-renewal**: ✅ Enabled

### Порты
- **Backend**: 8001
- **PostgreSQL**: 5433
- **Redis**: 6380

## 🗂 Структура файлов

```
backend/
├── 📖 Documentation/
│   ├── INDEX.md ← Вы здесь
│   ├── QUICKSTART.md
│   ├── README.md
│   ├── DEPLOYMENT.md
│   ├── ARCHITECTURE.md
│   ├── DOMAINS.md
│   ├── UPDATES_SUMMARY.md
│   ├── SETUP_SUMMARY.md
│   ├── PRODUCTION_CHECKLIST.md
│   └── PROMPT.md
│
├── 🐳 Docker/
│   ├── Dockerfile.prod
│   ├── docker compose.prod.yml
│   └── docker compose.yml
│
├── 🌐 Nginx/
│   ├── muscleup.conf
│   └── nginx.conf
│
├── 🚀 CI/CD/
│   └── .github/workflows/deploy.yml
│
├── 🛠 Scripts/
│   └── scripts/deploy/
│       ├── setup-server.sh
│       ├── setup-ssl.sh
│       ├── deploy.sh
│       └── rollback.sh
│
├── ⚙️  Configuration/
│   ├── .env.example
│   └── .env.production.example
│
└── 💻 Application/
    └── app/ (FastAPI code)
```

## 🎯 Как использовать эту документацию

### Сценарий 1: Первый деплой
1. Читать **QUICKSTART.md**
2. Следовать **PRODUCTION_CHECKLIST.md**
3. При проблемах → **DEPLOYMENT.md** (Troubleshooting)

### Сценарий 2: Настройка доменов
1. Читать **DOMAINS.md**
2. Запустить `setup-ssl.sh`

### Сценарий 3: Понять архитектуру
1. Читать **README.md** (обзор)
2. Углубиться в **ARCHITECTURE.md**

### Сценарий 4: Добавить новый проект
1. Скопировать **PROMPT.md** в новый проект
2. Открыть в Cursor AI
3. Следовать инструкциям

### Сценарий 5: Troubleshooting
1. **DEPLOYMENT.md** → раздел Troubleshooting
2. **DOMAINS.md** → SSL или DNS issues
3. Проверить логи: `docker logs muscleup_backend`

## ✅ Production Ready Checklist

Перед деплоем проверьте:
- [ ] DNS настроены для всех доменов
- [ ] GitHub Secrets добавлены
- [ ] `.env.production` создан на сервере
- [ ] SSL сертификат получен
- [ ] Health check работает

## 🆘 Получить помощь

- **GitHub Issues**: https://github.com/themilan1337/aitucup/issues
- **Email**: admin@muscleup.fitness
- **Документация**: Вы её читаете! 📖

## 📊 Статистика документации

- **Всего документов**: 11
- **Общий размер**: ~130KB
- **Последнее обновление**: 2026-01-16
- **Статус**: Production Ready ✅

---

**Tip**: Добавьте этот файл в закладки для быстрого доступа к документации!
