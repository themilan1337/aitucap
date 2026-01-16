# Production Domains Update Summary

## ✅ Все обновлено для production доменов!

### 🌐 Новые домены

**Landing**: https://muscleup.fitness
**Dashboard**: https://app.muscleup.fitness
**API**: https://api.muscleup.fitness ← SSL настраивается автоматически

**SSL Email**: admin@muscleup.fitness

---

## 📝 Обновленные файлы

### 1. Environment конфигурация

#### `.env.example` (Development)
✅ Обновлен для локальной разработки
- COOKIE_DOMAIN=localhost
- ALLOWED_ORIGINS включает localhost:3000, localhost:5173

#### `.env.production.example` (Production)
✅ Обновлен для production
- COOKIE_DOMAIN=api.muscleup.fitness
- ALLOWED_ORIGINS=https://muscleup.fitness,https://www.muscleup.fitness,https://app.muscleup.fitness

### 2. Nginx конфигурация

#### `nginx/muscleup.conf`
✅ Обновлены домены:
- server_name api.muscleup.fitness
- SSL certificates для api.muscleup.fitness
- WebSocket support для app.muscleup.fitness

### 3. Deployment скрипты

#### `scripts/deploy/setup-ssl.sh` ← **НОВЫЙ**
✅ Автоматическое получение SSL сертификата
- Domain: api.muscleup.fitness
- Email: admin@muscleup.fitness
- Автоматическая конфигурация Nginx
- Авто-обновление сертификата

#### `scripts/deploy/setup-server.sh`
✅ Обновлены инструкции для использования setup-ssl.sh

### 4. CI/CD

#### `.github/workflows/deploy.yml`
✅ Обновлены URL в deployment логах
- URL: https://api.muscleup.fitness

### 5. Документация

✅ Обновлены все упоминания доменов в:
- `README.md`
- `DEPLOYMENT.md`
- `SETUP_SUMMARY.md`

#### `DOMAINS.md` ← **НОВЫЙ**
✅ Полная документация по доменам:
- DNS конфигурация
- SSL setup инструкции
- CORS настройки
- Troubleshooting

---

## 🚀 Как использовать

### 1. Настройка DNS

Добавьте A-записи для всех доменов:

```
api.muscleup.fitness  →  YOUR_SERVER_IP
app.muscleup.fitness  →  YOUR_SERVER_IP
muscleup.fitness      →  YOUR_SERVER_IP
www.muscleup.fitness  →  YOUR_SERVER_IP
```

### 2. Установка сервера

```bash
# Первичная настройка
sudo bash scripts/deploy/setup-server.sh
```

### 3. Получение SSL сертификата

```bash
# Автоматическая настройка SSL для API
sudo bash scripts/deploy/setup-ssl.sh
```

Скрипт автоматически:
- ✅ Проверит DNS
- ✅ Установит Certbot
- ✅ Получит сертификат от Let's Encrypt
- ✅ Настроит Nginx
- ✅ Настроит авто-обновление

### 4. Настройка GitHub Secrets

Добавьте в Settings → Secrets → Actions:

```bash
SERVER_HOST=YOUR_SERVER_IP
SERVER_USER=your_username
SERVER_SSH_KEY=<private_ssh_key>

# Database
POSTGRES_PASSWORD=<strong_password>
DATABASE_URL=postgresql+asyncpg://...

# JWT
SECRET_KEY=<openssl rand -hex 32>
CSRF_SECRET_KEY=<openssl rand -hex 32>

# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://...

# Google OAuth
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_secret
```

### 5. Deploy

```bash
git add .
git commit -m "Update production domains"
git push origin main
```

GitHub Actions автоматически задеплоит на https://api.muscleup.fitness

---

## 🔒 SSL Сертификат

### Автоматическое обновление

Сертификат настроен на автообновление через systemd:

```bash
# Проверить статус
systemctl status certbot.timer

# Проверить сертификат
sudo certbot certificates

# Тестовое обновление
sudo certbot renew --dry-run
```

### Только для API

SSL сертификат настраивается **ТОЛЬКО** для `api.muscleup.fitness`:
- Landing (muscleup.fitness) - без SSL в этой конфигурации
- Dashboard (app.muscleup.fitness) - без SSL в этой конфигурации
- API (api.muscleup.fitness) - ✅ SSL автоматически

Landing и Dashboard должны иметь свой SSL (например, через Vercel/Netlify).

---

## ✅ Проверка

### 1. DNS

```bash
nslookup api.muscleup.fitness
```

### 2. SSL Certificate

```bash
curl -I https://api.muscleup.fitness/health
```

### 3. API Health

```bash
curl https://api.muscleup.fitness/health
```

Должно вернуть:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 4. CORS

```bash
curl -H "Origin: https://app.muscleup.fitness" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     https://api.muscleup.fitness/api/v1/auth/login/oauth -v
```

Должны быть заголовки:
```
Access-Control-Allow-Origin: https://app.muscleup.fitness
Access-Control-Allow-Credentials: true
```

---

## 📋 Checklist

- [ ] DNS записи настроены
- [ ] Сервер настроен (`setup-server.sh`)
- [ ] SSL получен (`setup-ssl.sh`)
- [ ] `.env.production` создан на сервере
- [ ] GitHub Secrets настроены
- [ ] Первый deploy выполнен
- [ ] API health check работает
- [ ] CORS работает с app.muscleup.fitness

---

## 🎯 Production URLs

После деплоя:

- **API Health**: https://api.muscleup.fitness/health
- **API Docs**: https://api.muscleup.fitness/docs
- **WebSocket**: wss://api.muscleup.fitness/api/v1/vision/ws/pose

Frontend должен использовать:
```typescript
const API_BASE_URL = 'https://api.muscleup.fitness'
const WS_BASE_URL = 'wss://api.muscleup.fitness'
```

---

**Дата обновления**: 2026-01-16
**SSL Email**: admin@muscleup.fitness
**Статус**: ✅ Production Ready
