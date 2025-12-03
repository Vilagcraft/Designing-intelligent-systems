# 🚀 Руководство по развертыванию

## Production deployment

### Требования

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM минимум
- 10GB свободного места

---

## 🐳 Быстрый старт с Docker

### 1. Production режим

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Vilagcraft/Designing-intelligent-systems.git
cd Designing-intelligent-systems

# 2. Скопировать и настроить переменные окружения
cp env.example .env
# Отредактируйте .env файл

# 3. Запустить сервисы
docker-compose up -d

# 4. Проверить логи
docker-compose logs -f

# 5. Проверить статус
docker-compose ps
```

**Доступ:**
- Frontend: http://localhost
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### 2. Development режим

```bash
# Запуск в dev режиме с hot reload
docker-compose -f docker-compose.dev.yml up
```

---

## 📦 Команды Docker Compose

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Просмотр логов
docker-compose logs -f [service_name]

# Выполнить команду в контейнере
docker-compose exec backend python manage.py

# Пересобрать образы
docker-compose build --no-cache

# Обновить и перезапустить
docker-compose pull && docker-compose up -d
```

---

## 🔧 Настройка для production

### 1. Переменные окружения

Создайте `.env` файл:

```bash
ENVIRONMENT=production
LOG_LEVEL=INFO
BACKEND_WORKERS=4
CORS_ORIGINS=https://yourdomain.com
```

### 2. Настройка nginx (опционально)

Если используете внешний nginx:

```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. SSL/HTTPS

Используйте Let's Encrypt:

```bash
# Установка certbot
sudo apt-get install certbot python3-certbot-nginx

# Получение сертификата
sudo certbot --nginx -d yourdomain.com
```

---

## 🔄 CI/CD

### GitHub Actions

Pipeline автоматически:
1. Тестирует код
2. Проверяет качество (linting)
3. Собирает Docker образы
4. Публикует в Docker Hub
5. Деплоит на сервер

**Настройка secrets:**

В GitHub → Settings → Secrets добавьте:
- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `SERVER_HOST`
- `SERVER_USER`
- `SERVER_SSH_KEY`

---

## 📊 Мониторинг

### Docker healthchecks

```bash
# Проверка здоровья контейнеров
docker ps

# Детальная информация
docker inspect sentiment-backend | grep -A 5 "Health"
```

### Логи

```bash
# Все логи
docker-compose logs -f

# Только Backend
docker-compose logs -f backend

# Только Frontend
docker-compose logs -f frontend

# Последние 100 строк
docker-compose logs --tail=100
```

---

## 🔒 Безопасность

### 1. Firewall

```bash
# UFW на Ubuntu
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

### 2. Docker security

- ✅ Non-root пользователь в контейнерах
- ✅ Read-only файловые системы где возможно
- ✅ Ограничение ресурсов
- ✅ Сканирование образов на уязвимости

```bash
# Сканирование образа
docker scan sentiment-backend:latest
```

### 3. Обновления

```bash
# Регулярно обновляйте образы
docker-compose pull
docker-compose up -d
```

---

## 📈 Масштабирование

### Horizontal scaling

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

### Load balancer

Используйте nginx для балансировки:

```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

---

## 🐛 Troubleshooting

### Проблема: Контейнер не запускается

```bash
# Проверить логи
docker-compose logs backend

# Войти в контейнер
docker-compose exec backend sh

# Пересобрать
docker-compose build --no-cache backend
docker-compose up -d
```

### Проблема: Out of memory

```bash
# Увеличить лимиты в docker-compose.yml
services:
  backend:
    mem_limit: 2g
```

### Проблема: Модель не загружается

```bash
# Проверить volume
docker volume ls
docker volume inspect sentiment_models

# Пересоздать volume
docker-compose down -v
docker-compose up -d
```

---

## 🔄 Резервное копирование

### Модели

```bash
# Backup
docker run --rm -v sentiment_models:/data -v $(pwd):/backup \
  alpine tar czf /backup/models-backup.tar.gz /data

# Restore
docker run --rm -v sentiment_models:/data -v $(pwd):/backup \
  alpine tar xzf /backup/models-backup.tar.gz -C /
```

### База данных (если используется)

```bash
# Backup PostgreSQL
docker-compose exec postgres pg_dump -U user dbname > backup.sql

# Restore
docker-compose exec -T postgres psql -U user dbname < backup.sql
```

---

## 📞 Поддержка

**Документация:**
- [README.md](README.md) - общая информация
- [DOCKER.md](DOCKER.md) - детали Docker
- [API Documentation](http://localhost:8000/docs) - после запуска

**Логи и мониторинг:**
- Логи: `docker-compose logs`
- Метрики: Prometheus (если настроен)
- Трейсинг: Jaeger (если настроен)

---

**Успешного деплоя! 🚀**

