# Production Deployment Checklist

> Используйте этот чеклист для деплоя на production

## Pre-Deployment

### 1. DNS Configuration
- [ ] A record для `muscleup.fitness` → SERVER_IP
- [ ] A record для `www.muscleup.fitness` → SERVER_IP
- [ ] A record для `app.muscleup.fitness` → SERVER_IP
- [ ] A record для `api.muscleup.fitness` → SERVER_IP
- [ ] Проверить DNS propagation: `nslookup api.muscleup.fitness`

### 2. Server Access
- [ ] SSH доступ к Ubuntu серверу работает
- [ ] У вас есть sudo права
- [ ] Сервер соответствует минимальным требованиям:
  - [ ] Ubuntu 20.04+ (рекомендуется 22.04)
  - [ ] 2GB+ RAM
  - [ ] 2+ CPU cores
  - [ ] 20GB+ disk space

### 3. Secrets Preparation
- [ ] Сгенерирован `POSTGRES_PASSWORD`: `openssl rand -base64 32`
- [ ] Сгенерирован `SECRET_KEY`: `openssl rand -hex 32`
- [ ] Сгенерирован `CSRF_SECRET_KEY`: `openssl rand -hex 32`
- [ ] Есть Azure OpenAI API key
- [ ] Есть Google OAuth credentials

### 4. SSH Key Generation
- [ ] Сгенерирован SSH ключ для deploy:
  ```bash
  ssh-keygen -t ed25519 -C "github-deploy" -f ~/.ssh/muscleup_deploy -N ""
  ```
- [ ] Публичный ключ скопирован на сервер:
  ```bash
  ssh-copy-id -i ~/.ssh/muscleup_deploy.pub ubuntu@SERVER_IP
  ```
- [ ] Проверен доступ: `ssh -i ~/.ssh/muscleup_deploy ubuntu@SERVER_IP`

## Server Setup

### 5. Initial Server Configuration
- [ ] Склонирован репозиторий на сервер
- [ ] Запущен `sudo bash scripts/deploy/setup-server.sh`
- [ ] Установка завершилась успешно
- [ ] Docker работает: `docker ps`
- [ ] Nginx работает: `systemctl status nginx`
- [ ] Firewall настроен: `ufw status` (80, 443, 22 открыты)

### 6. SSL Certificate
- [ ] Запущен `sudo bash scripts/deploy/setup-ssl.sh`
- [ ] Сертификат получен успешно
- [ ] Nginx перезагружен автоматически
- [ ] Проверен сертификат: `curl -I https://api.muscleup.fitness/health`
- [ ] Настроено авто-обновление: `systemctl status certbot.timer`

### 7. Environment Configuration
- [ ] Создан `/opt/projects/muscleup/.env.production`:
  ```bash
  sudo nano /opt/projects/muscleup/.env.production
  ```
- [ ] Заполнены все переменные окружения
- [ ] Установлены правильные permissions:
  ```bash
  sudo chmod 600 /opt/projects/muscleup/.env.production
  ```
- [ ] Проверены настройки:
  - [ ] `COOKIE_DOMAIN=api.muscleup.fitness`
  - [ ] `ALLOWED_ORIGINS` содержит все frontend домены
  - [ ] `ENVIRONMENT=production`
  - [ ] `LOG_LEVEL=info`

## GitHub Configuration

### 8. GitHub Secrets
Перейти в **Settings → Secrets and variables → Actions**

**Server Connection:**
- [ ] `SERVER_HOST` = ваш SERVER_IP
- [ ] `SERVER_USER` = ubuntu
- [ ] `SERVER_SSH_KEY` = приватный ключ
- [ ] `SERVER_PORT` = 22 (опционально)

**Database:**
- [ ] `POSTGRES_PASSWORD`
- [ ] `DATABASE_URL`

**Redis:**
- [ ] `REDIS_URL`

**Security:**
- [ ] `SECRET_KEY`
- [ ] `CSRF_SECRET_KEY`

**Azure OpenAI:**
- [ ] `AZURE_OPENAI_API_KEY`
- [ ] `AZURE_OPENAI_ENDPOINT`
- [ ] `AZURE_OPENAI_DEPLOYMENT`
- [ ] `AZURE_OPENAI_API_VERSION`

**Google OAuth:**
- [ ] `GOOGLE_CLIENT_ID`
- [ ] `GOOGLE_CLIENT_SECRET`

**Docker Hub (опционально):**
- [ ] `DOCKER_USERNAME`
- [ ] `DOCKER_PASSWORD`

## First Deployment

### 9. Deploy
- [ ] Все изменения закоммичены:
  ```bash
  git add .
  git commit -m "Configure production domains and SSL"
  ```
- [ ] Push в main branch:
  ```bash
  git push origin main
  ```
- [ ] GitHub Actions workflow запустился
- [ ] Все jobs прошли успешно:
  - [ ] Test & Lint
  - [ ] Build Docker Image
  - [ ] Deploy to Server

### 10. Verification

**API Health:**
- [ ] `curl https://api.muscleup.fitness/health` возвращает 200 OK
- [ ] Response содержит `"status": "healthy"`

**SSL:**
- [ ] HTTPS работает без предупреждений
- [ ] HTTP редиректит на HTTPS
- [ ] Сертификат валиден в браузере

**CORS:**
- [ ] Проверен CORS для app.muscleup.fitness:
  ```bash
  curl -H "Origin: https://app.muscleup.fitness" \
       -H "Access-Control-Request-Method: POST" \
       -X OPTIONS \
       https://api.muscleup.fitness/api/v1/auth/login/oauth -v
  ```
- [ ] Заголовки `Access-Control-Allow-Origin` присутствуют

**Docker Containers:**
- [ ] `docker ps | grep muscleup` показывает 3 контейнера
- [ ] muscleup_backend - UP
- [ ] muscleup_postgres - UP
- [ ] muscleup_redis - UP

**Logs:**
- [ ] Логи backend чистые: `docker logs muscleup_backend`
- [ ] Нет критических ошибок
- [ ] Database подключена
- [ ] Redis подключен

### 11. API Endpoints Testing

- [ ] `/health` - Health check
- [ ] `/docs` - API documentation (Swagger UI)
- [ ] `/api/v1/auth/*` - Authentication endpoints
- [ ] WebSocket connection работает (если необходимо)

### 12. Monitoring Setup

**Manual Checks:**
- [ ] Настроен мониторинг uptime (например, UptimeRobot)
- [ ] Настроены уведомления при downtime

**Log Rotation:**
- [ ] Проверить настройки rotation: `/etc/logrotate.d/muscleup`

**Backups:**
- [ ] Настроено резервное копирование БД
- [ ] Проверен доступ к backups: `/opt/projects/muscleup/backups/`

## Post-Deployment

### 13. Documentation
- [ ] Обновлен README.md с production URLs
- [ ] Команда знает про API URL: `https://api.muscleup.fitness`
- [ ] Frontend настроен на использование production API

### 14. Security Review
- [ ] Firewall настроен правильно
- [ ] Только необходимые порты открыты
- [ ] SSH доступ ограничен (желательно key-only)
- [ ] Fail2Ban работает: `systemctl status fail2ban`
- [ ] Secrets не в git репозитории
- [ ] `.env.production` имеет permissions 600

### 15. Performance
- [ ] API отвечает быстро (<500ms)
- [ ] WebSocket соединения стабильны
- [ ] Нет memory leaks
- [ ] CPU usage нормальный

### 16. Testing with Frontend
- [ ] Frontend успешно подключается к API
- [ ] OAuth авторизация работает
- [ ] CSRF защита не блокирует запросы
- [ ] Cookies устанавливаются корректно
- [ ] WebSocket для real-time features работает

## Troubleshooting

### If Something Goes Wrong

**SSL Issues:**
```bash
sudo certbot certificates
sudo certbot renew --dry-run
sudo nginx -t
sudo systemctl reload nginx
```

**Backend Issues:**
```bash
docker logs muscleup_backend
docker-compose -f /opt/projects/muscleup/current/docker-compose.prod.yml restart
```

**Rollback:**
```bash
sudo bash /path/to/backend/scripts/deploy/rollback.sh
```

**GitHub Actions Failed:**
- Check logs in Actions tab
- Verify all secrets are set
- Test SSH connection manually
- Check server logs

## Success Criteria

✅ Deployment считается успешным когда:

1. SSL сертификат установлен и работает
2. API health check возвращает 200 OK
3. Все Docker контейнеры UP
4. CORS работает с frontend доменами
5. GitHub Actions deploy успешно завершился
6. Frontend может подключиться к API
7. OAuth авторизация работает
8. Нет критических ошибок в логах

## Next Steps

После успешного деплоя:

1. Настроить monitoring и alerting
2. Документировать процесс для команды
3. Настроить регулярные backups
4. Провести load testing
5. Настроить staging environment (опционально)

---

**Последнее обновление**: 2026-01-16
**Версия**: 1.0
**Контакт**: admin@muscleup.fitness
