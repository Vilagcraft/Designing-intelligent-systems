# 🐳 Docker руководство

## Архитектура

```
┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │
│    Frontend     │◄───────►│     Backend     │
│   (nginx:80)    │         │   (uvicorn:8000)│
│                 │         │                 │
└─────────────────┘         └─────────────────┘
        │                           │
        └───────────┬───────────────┘
                    │
              sentiment-network
                    │
              ┌─────▼─────┐
              │  Volumes  │
              │  (models) │
              └───────────┘
```

---

## 📦 Структура образов

### Backend Image
**Базовый образ:** `python:3.10-slim`  
**Размер:** ~500MB  
**Особенности:**
- Multi-stage build для оптимизации
- Non-root пользователь
- Healthcheck встроен
- Production-ready с uvicorn + 4 workers

### Frontend Image
**Базовый образ:** `node:18-alpine` → `nginx:alpine`  
**Размер:** ~25MB  
**Особенности:**
- Multi-stage build
- Статика на nginx
- Gzip compression
- Security headers
- SPA routing

---

## 🚀 Команды

### Production

```bash
# Запуск
docker-compose up -d

# Проверка статуса
docker-compose ps

# Логи в реальном времени
docker-compose logs -f

# Остановка
docker-compose down

# Остановка с удалением volumes
docker-compose down -v
```

### Development

```bash
# Запуск с hot reload
docker-compose -f docker-compose.dev.yml up

# Запуск только backend
docker-compose -f docker-compose.dev.yml up backend

# Запуск только frontend
docker-compose -f docker-compose.dev.yml up frontend
```

### Сборка

```bash
# Пересобрать все образы
docker-compose build

# Пересобрать без кэша
docker-compose build --no-cache

# Пересобрать конкретный сервис
docker-compose build backend

# Пересобрать и запустить
docker-compose up -d --build
```

---

## 🔍 Отладка

### Войти в контейнер

```bash
# Backend
docker-compose exec backend sh

# Frontend
docker-compose exec frontend sh

# Или через docker
docker exec -it sentiment-backend sh
```

### Проверить логи

```bash
# Все логи
docker-compose logs

# Последние 100 строк
docker-compose logs --tail=100

# Конкретный сервис
docker-compose logs backend

# С отслеживанием
docker-compose logs -f backend
```

### Проверить ресурсы

```bash
# Использование ресурсов
docker stats

# Детали контейнера
docker inspect sentiment-backend

# Healthcheck статус
docker inspect --format='{{.State.Health.Status}}' sentiment-backend
```

---

## 📊 Мониторинг

### Healthchecks

**Backend:**
```bash
curl http://localhost:8000/health
```

Ответ:
```json
{
  "model": true,
  "vocab": true,
  "status": "ok"
}
```

**Frontend:**
```bash
curl http://localhost
```

### Docker events

```bash
# Отслеживание событий
docker events --filter 'container=sentiment-backend'

# С фильтрами
docker events --filter 'event=start' --filter 'event=stop'
```

---

## 🔧 Конфигурация

### Переменные окружения

Создайте `.env`:

```bash
# Production
ENVIRONMENT=production
LOG_LEVEL=INFO
BACKEND_WORKERS=4

# Development
ENVIRONMENT=development
LOG_LEVEL=DEBUG
BACKEND_WORKERS=1
```

### Ограничение ресурсов

Добавьте в `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

---

## 🔒 Безопасность

### Сканирование на уязвимости

```bash
# Trivy
trivy image sentiment-backend:latest

# Docker scan
docker scan sentiment-backend:latest
```

### Best practices

✅ **Используется:**
- Non-root пользователь
- Multi-stage build
- Минимальные базовые образы
- .dockerignore файлы
- Healthchecks

⚠️ **TODO для production:**
- [ ] Secrets management (не в образе!)
- [ ] Image signing
- [ ] Registry security
- [ ] Network policies

---

## 📦 Volumes

### Управление данными

```bash
# Список volumes
docker volume ls

# Детали volume
docker volume inspect sentiment_models

# Backup volume
docker run --rm -v sentiment_models:/data -v $(pwd):/backup \
  alpine tar czf /backup/models-backup.tar.gz /data

# Restore volume
docker run --rm -v sentiment_models:/data -v $(pwd):/backup \
  alpine tar xzf /backup/models-backup.tar.gz -C /

# Удалить volume
docker volume rm sentiment_models
```

---

## 🌐 Networking

### Проверка сети

```bash
# Список сетей
docker network ls

# Детали сети
docker network inspect sentiment-network

# Проверить connectivity
docker-compose exec backend ping frontend
docker-compose exec frontend ping backend
```

### DNS resolution

В Docker Compose сервисы доступны по имени:
- `backend` → backend:8000
- `frontend` → frontend:80

---

## 🔄 CI/CD Integration

### Build в CI

```yaml
# .github/workflows/ci-cd.yml
- name: Build image
  run: docker build -t sentiment-backend:${{ github.sha }} ./Realization/Backend
```

### Push в registry

```bash
# Docker Hub
docker tag sentiment-backend:latest username/sentiment-backend:latest
docker push username/sentiment-backend:latest

# GitHub Container Registry
docker tag sentiment-backend:latest ghcr.io/username/sentiment-backend:latest
docker push ghcr.io/username/sentiment-backend:latest
```

---

## 🐛 Troubleshooting

### Проблемы и решения

#### 1. Port already in use

```bash
# Найти процесс
sudo lsof -i :8000

# Убить процесс
sudo kill -9 <PID>

# Или изменить порт в docker-compose.yml
ports:
  - "8001:8000"
```

#### 2. Out of disk space

```bash
# Очистить неиспользуемые образы
docker image prune -a

# Очистить всё
docker system prune -a --volumes

# Проверить использование
docker system df
```

#### 3. Container restarts constantly

```bash
# Проверить логи
docker-compose logs --tail=50 backend

# Проверить healthcheck
docker inspect --format='{{json .State.Health}}' sentiment-backend

# Отключить автоперезапуск временно
docker update --restart=no sentiment-backend
```

#### 4. Cannot connect to Docker daemon

```bash
# Запустить Docker
sudo systemctl start docker

# Добавить пользователя в группу
sudo usermod -aG docker $USER
newgrp docker
```

---

## 📈 Производительность

### Оптимизация образов

```dockerfile
# ❌ Плохо
RUN apt-get update
RUN apt-get install -y package1
RUN apt-get install -y package2

# ✅ Хорошо
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*
```

### Кэширование слоев

```dockerfile
# Копируем requirements сначала для кэширования
COPY requirements.txt .
RUN pip install -r requirements.txt

# Потом код (чаще меняется)
COPY . .
```

### Build cache

```bash
# Использовать BuildKit
DOCKER_BUILDKIT=1 docker build .

# Или в docker-compose
COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 docker-compose build
```

---

## 📚 Дополнительные ресурсы

- [Docker docs](https://docs.docker.com/)
- [Docker Compose docs](https://docs.docker.com/compose/)
- [Best practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Успешной работы с Docker! 🐳**

