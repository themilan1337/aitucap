# MuscleUp - Workout System Integration Guide

Полная интеграция системы тренировок из Good-GYM-master в проект MuscleUp.

## Что было реализовано

### Backend (FastAPI)
- ✅ **RTMPose Processor** - Обработка pose detection с ONNX моделями
- ✅ **Exercise Counter** - Автоматический подсчет повторений для 12 упражнений
- ✅ **Vision API** - WebSocket endpoint для real-time pose detection
- ✅ **ONNX Models** - 4 модели (89 MB): yolox_nano, rtmpose-t/s/m
- ✅ **Exercises Config** - JSON конфигурация всех упражнений

### Frontend (Nuxt 4 + Vue 3)
- ✅ **WorkoutCamera.vue** - Полностью переписан с real-time detection
- ✅ **WebSocket Integration** - Отправка video frames и получение keypoints
- ✅ **Skeleton Visualization** - Canvas overlay с цветными соединениями
- ✅ **Real-time Rep Counting** - Подсчет повторений с backend
- ✅ **Angle Display** - Визуализация работающих углов суставов

## Архитектура решения

```
┌─────────────┐                    ┌──────────────┐
│  Dashboard  │                    │   Backend    │
│  (Nuxt 4)   │                    │  (FastAPI)   │
└──────┬──────┘                    └──────┬───────┘
       │                                  │
       │  1. Video Frame (base64)        │
       │  ────────────────────────────>   │
       │                                  │
       │                                  │  2. RTMPose
       │                                  │     Detection
       │                                  │
       │  3. Keypoints + Reps + Angle    │
       │  <────────────────────────────   │
       │                                  │
       │  4. Draw Skeleton on Canvas     │
       │                                  │
       └──────────────────────────────────┘
              WebSocket Connection
```

## Установка и Запуск

### 1. Backend Setup

**Option A: Docker (Recommended)**
```bash
cd /Users/milan/Documents/GitHub/aitucup/backend

# Запустите все сервисы (PostgreSQL, Redis, Backend)
docker-compose up -d --build

# Проверьте статус
docker-compose ps

# Проверьте логи
docker-compose logs backend

# Проверьте health
curl http://localhost:8000/api/v1/vision/health
```

**Option B: Local Development**
```bash
cd /Users/milan/Documents/GitHub/aitucup/backend

# Установите зависимости (включая vision libraries)
pip install -r requirements.txt

# Убедитесь что models и data directories существуют
ls -lh models/  # Должно быть 4 .onnx файла (89 MB)
ls data/        # Должен быть exercises.json

# Запустите backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Important Notes:**
- Used `opencv-python-headless==4.10.0.84` (no GUI dependencies for Docker)
- Used `rtmlib==0.0.13` (compatible with numpy 1.26.4)
- All dependencies are now ARM64-compatible (Apple Silicon)

### 2. Dashboard Setup

```bash
cd /Users/milan/Documents/GitHub/aitucup/dashboard

# Установите зависимости
pnpm install

# Запустите dev server
pnpm dev
```

### 3. Проверка работы

1. Откройте http://localhost:3000
2. Войдите через Google OAuth
3. Пройдите onboarding (если нужно)
4. Перейдите на страницу `/train`
5. Нажмите "Начать тренировку"
6. **Разрешите доступ к камере**
7. Вы должны увидеть:
   - Video stream с вашим изображением
   - **Skeleton overlay** (цветные линии и точки)
   - Real-time rep counter
   - Angle display
   - Connection status "Подключение к серверу..." → исчезнет когда подключится

## API Endpoints

### Vision API

- **WebSocket**: `ws://localhost:8000/api/v1/vision/ws/pose`
  - Отправка: `{ "frame": "base64_image", "exercise": "squat" }`
  - Получение: `{ "success": true, "keypoints": [[x,y], ...], "reps": 10, "angle": 145.2 }`

- **GET** `/api/v1/vision/health` - Health check
- **GET** `/api/v1/vision/exercises` - Список поддерживаемых упражнений
- **POST** `/api/v1/vision/reset-counter` - Сброс счетчика повторений

## Поддерживаемые упражнения

| ID | Название (RU) | Название (EN) | Тип |
|----|--------------|---------------|-----|
| squat | Приседания | Squat | Ноги |
| lunge | Выпады | Lunge | Ноги |
| pushup | Отжимания | Push-up | Руки |
| plank | Планка | Plank | Корпус |
| situp | Пресс | Sit-up | Корпус |
| crunch | Скручивания | Crunch | Корпус |
| bicep_curl | Подъем на бицепс | Bicep Curl | Руки |
| lateral_raise | Разведение рук | Lateral Raise | Плечи |
| overhead_press | Жим вверх | Overhead Press | Плечи |
| leg_raise | Подъем ног | Leg Raise | Пресс |
| knee_raise | Подъем коленей | Knee Raise | Пресс |
| knee_press | Сгибание коленей | Knee Press | Ноги |

## Skeleton Visualization

### COCO 17 Keypoints Format
```
0: nose
1: left_eye          2: right_eye
3: left_ear          4: right_ear
5: left_shoulder     6: right_shoulder
7: left_elbow        8: right_elbow
9: left_wrist        10: right_wrist
11: left_hip         12: right_hip
13: left_knee        14: right_knee
15: left_ankle       16: right_ankle
```

### Color Scheme
- **Head**: Blue (#3399FF)
- **Torso**: Orange (#FF9933)
- **Arms**: Green (#99FF33)
- **Legs**: Pink (#FF3399)
- **Keypoints**: Neon (#CCFF00)
- **Angle Lines**: Yellow (#FFFF00)

## Производительность

- **Frame Rate**: 10 FPS (100ms interval)
- **Image Quality**: JPEG 70%
- **Resolution**: 1280x720 (camera) → 640x360 (inference)
- **Latency**: ~100-200ms (зависит от CPU)

## Troubleshooting

### Backend не запускается
```bash
# Проверьте установку rtmlib
pip install rtmlib

# Проверьте наличие моделей
ls -lh backend/models/*.onnx
```

### WebSocket не подключается
- Убедитесь что backend запущен на порту 8000
- Проверьте `NUXT_PUBLIC_API_URL` в dashboard
- Откройте DevTools → Network → WS и проверьте ошибки

### Skeleton не отображается
- Убедитесь что камера работает
- Проверьте console.log для ошибок
- Убедитесь что вы находитесь в кадре целиком
- Попробуйте лучшее освещение

### Низкая производительность
- Используйте `mode='lightweight'` в `get_rtmpose_processor()`
- Уменьшите frame rate в `startSendingFrames()` (например, 200ms)
- Уменьшите качество JPEG (например, 0.5)

## Структура файлов

```
backend/
├── app/
│   ├── workouts/
│   │   ├── __init__.py
│   │   ├── exercise_counter.py      ✨ NEW
│   │   └── rtmpose_processor.py     ✨ NEW
│   ├── api/v1/
│   │   └── vision.py                ✨ NEW
│   └── main.py                      📝 Updated
├── models/                          ✨ NEW
│   ├── yolox_nano_*.onnx           (3.5 MB)
│   ├── rtmpose-t_*.onnx            (13 MB)
│   ├── rtmpose-s_*.onnx            (21 MB)
│   └── rtmpose-m_*.onnx            (52 MB)
├── data/                            ✨ NEW
│   └── exercises.json
└── requirements.txt                 📝 Updated

dashboard/
└── app/
    └── components/workout/
        └── WorkoutCamera.vue        ✨ Fully Rewritten
```

## Следующие шаги

### Рекомендуемые улучшения:
1. **Form Quality Analysis** - Реальная оценка техники выполнения
2. **Multi-person Detection** - Поддержка нескольких людей в кадре
3. **Exercise Auto-detection** - Автоматическое определение типа упражнения
4. **Voice Feedback** - Голосовые подсказки по технике
5. **Workout Saving** - Сохранение результатов в базу через `/api/v1/workouts`
6. **Video Recording** - Запись видео тренировки
7. **Performance Optimization** - WebWorkers для обработки frames

### Оптимизация:
- [ ] Добавить кэширование frames на клиенте
- [ ] Использовать WebWorkers для capture frames
- [ ] Оптимизировать canvas rendering (requestAnimationFrame)
- [ ] Добавить rate limiting на WebSocket
- [ ] Implement model warm-up на backend startup

## Credits

- **Original Project**: Good-GYM-master
- **Pose Detection**: RTMPose (rtmlib)
- **Framework**: FastAPI + Nuxt 4 + Vue 3
- **Integration**: Claude Code

---

## Quick Start Commands

```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Dashboard
cd dashboard && pnpm dev

# Open browser
open http://localhost:3000/train
```

**Enjoy your AI-powered workout! 💪🤖**
