# MuscleUp Vision

Проект разработан в рамках **AITU CAP 2 тур**.

## О проекте

**MuscleUp Vision** - это фитнес-платформа с искусственным интеллектом, которая использует компьютерное зрение для анализа техники выполнения упражнений в реальном времени.

### Возможности

- **Анализ в реальном времени** - Компьютерное зрение отслеживает движения и анализирует технику выполнения упражнений мгновенно
- **ИИ-тренер** - Искусственный интеллект дает рекомендации и корректирует технику как персональный тренер
- **Персональный план** - Индивидуальная программа тренировок, адаптированная под ваш уровень и цели
- **Отслеживание прогресса** - Подробная статистика тренировок, калорий и достижений

### Как это работает

1. **Камера определяет положение тела** - Технология компьютерного зрения распознает ключевые точки тела
2. **ИИ анализирует технику** - Нейросеть оценивает правильность выполнения упражнения в реальном времени
3. **Приложение подсказывает** - Мгновенная обратная связь при нарушении техники

## Структура проекта

```
aitucup/
├── backend/          # FastAPI бэкенд с Computer Vision
├── dashboard/        # Nuxt.js веб-приложение для тренировок
├── landing/          # Лендинг страница
└── ios/              # iOS приложение
```

## Технологический стек

### Backend
- **Python 3.11** - Язык программирования
- **FastAPI** - Асинхронный веб-фреймворк
- **PostgreSQL 15** - База данных
- **Redis 7** - Кэш и сессии
- **Azure OpenAI** - AI интеграция
- **MediaPipe** - Computer Vision для детекции поз

### Frontend
- **Nuxt.js** - Vue.js фреймворк
- **TailwindCSS** - CSS фреймворк
- **TypeScript** - Типизированный JavaScript

### Infrastructure
- **Docker** - Контейнеризация
- **Nginx** - Reverse proxy
- **GitHub Actions** - CI/CD

## Запуск проекта

### Backend

```bash
cd backend
cp .env.example .env
# Заполните .env файл

# С Docker
docker-compose up -d

# Или локально
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Dashboard

```bash
cd dashboard
pnpm install
pnpm dev
```

### Landing

```bash
cd landing
pnpm install
pnpm dev
```

## API

Документация API доступна по адресу `/docs` (Swagger UI)

### Основные endpoints

- `POST /api/v1/auth/login/oauth` - OAuth авторизация
- `POST /api/v1/plans/generate` - Генерация плана тренировок (AI)
- `WS /api/v1/vision/ws/pose` - WebSocket для real-time детекции поз
- `GET /api/v1/workouts/history` - История тренировок

## Команда

Проект создан командой:
- **Milan**
- **Bizhan**
- **Sultan**

---

**AITU CAP 2026**
