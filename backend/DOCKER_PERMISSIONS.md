# Docker Permissions Fix

> Решение проблемы "permission denied" при работе с Docker

## Проблема

После установки Docker видите ошибку:
```
Got permission denied while trying to connect to the Docker daemon socket
```

Или:
```
docker: permission denied
```

## Причина

Ваш пользователь был добавлен в группу `docker`, но изменения групп не применяются к текущей сессии автоматически. Нужно перелогиниться.

## ✅ Решение 1: Перелогиниться (Рекомендуется)

Это самый правильный способ:

```bash
# Выйти из SSH сессии
exit

# Войти заново
ssh user@your-server

# Проверить что работает
docker ps
```

## ✅ Решение 2: Применить изменения без перелогина

Если не хотите выходить:

```bash
# Вариант A: Применить новую группу
newgrp docker

# Вариант B: Создать новую login shell
su - $USER

# Проверить
docker ps
```

## ✅ Решение 3: Использовать sudo (временно)

До перелогина можете использовать sudo:

```bash
# Временно используйте sudo
sudo docker ps
sudo docker compose up -d
```

⚠️ **Не рекомендуется** для постоянного использования!

## Как проверить что проблема решена?

```bash
# Должно работать БЕЗ sudo
docker ps

# Должно показать список контейнеров (или пустой список)
# Если видите "permission denied" - нужно перелогиниться
```

## Проверить группы пользователя

```bash
# Посмотреть в каких группах вы состоите
groups

# Должна быть группа "docker"
# Пример вывода: ubuntu adm cdrom sudo dip plugdev lxd docker
```

```bash
# Детальная информация
id

# Должно быть: groups=...,999(docker)
```

## Если всё равно не работает

### 1. Проверить что Docker daemon запущен

```bash
sudo systemctl status docker

# Должно быть: Active: active (running)
```

Если не запущен:
```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. Проверить что группа docker существует

```bash
getent group docker

# Должно вывести: docker:x:999:username
```

Если группы нет:
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
```

### 3. Проверить права на Docker socket

```bash
ls -la /var/run/docker.sock

# Должно быть: srw-rw---- 1 root docker ... /var/run/docker.sock
```

Если права неправильные:
```bash
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock
```

### 4. Перезапустить Docker service

```bash
sudo systemctl restart docker
```

## Автоматическое исправление

Если ничего не помогает, запустите:

```bash
#!/bin/bash
# Скрипт автоматического исправления

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER

# Исправить права на socket
sudo chown root:docker /var/run/docker.sock
sudo chmod 660 /var/run/docker.sock

# Перезапустить Docker
sudo systemctl restart docker

echo "Теперь выйдите и войдите заново: exit, затем ssh user@server"
```

## Для GitHub Actions / CI/CD

В CI/CD environments используйте sudo, так как там нет persistent сессий:

```yaml
# В .github/workflows/deploy.yml
- name: Run Docker
  run: |
    sudo docker ps
    sudo docker compose up -d
```

Или используйте Docker-in-Docker:

```yaml
services:
  docker:
    image: docker:latest
```

## Security Note

⚠️ **Важно**: Добавление пользователя в группу `docker` даёт ему root-эквивалентные права, так как он может запускать контейнеры с root privileges.

Это нормально для:
- Development окружений
- Trusted administrators
- CI/CD systems

Не добавляйте в группу docker:
- Недоверенных пользователей
- Публичные аккаунты
- Пользователей без sudo доступа

## Альтернатива: Rootless Docker

Для повышенной безопасности можно использовать rootless Docker:

```bash
# Установка rootless Docker
curl -fsSL https://get.docker.com/rootless | sh

# Настройка
systemctl --user start docker
systemctl --user enable docker

# Добавить в PATH
export PATH=/home/$USER/bin:$PATH
export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock
```

## Полезные команды

```bash
# Показать Docker info
docker info

# Показать версию
docker --version

# Показать процессы
docker ps -a

# Показать образы
docker images

# Показать сети
docker network ls

# Показать volumes
docker volume ls
```

## Если используете VSCode Remote SSH

После добавления в группу docker:

1. Закройте все VSCode окна
2. Перезапустите VSCode
3. Переподключитесь к серверу

Или в VSCode терминале:
```bash
newgrp docker
```

## Summary

**Самый простой способ:**

```bash
exit              # Выйти
ssh user@server   # Войти обратно
docker ps         # Проверить
```

**Если нельзя выйти:**

```bash
newgrp docker     # Применить группу
docker ps         # Проверить
```

**Временно:**

```bash
sudo docker ps    # Использовать sudo
```

---

**Эта проблема нормальна** после первой установки Docker. Просто перелогиньтесь и всё будет работать!
