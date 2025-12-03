# 🚀 Деплой на Render.com

Пошаговое руководство по развертыванию системы анализа тональности на Render.com.

---

## 📋 Подготовка

### Требования:
- Аккаунт на [Render.com](https://render.com)
- GitHub репозиторий с кодом
- Git настроен и код запушен

### Что будет задеплоено:
- ✅ Backend (FastAPI) - Web Service
- ✅ Frontend (Vue + nginx) - Static Site
- ✅ Automatic HTTPS
- ✅ Environment variables

---

## 🎯 Шаг 1: Подготовка файлов

### 1.1 Создайте render.yaml

Этот файл уже создан в корне проекта и содержит всю конфигурацию.

### 1.2 Проверьте Dockerfiles

Убедитесь, что файлы на месте:
- ✅ `Realization/Backend/Dockerfile`
- ✅ `Realization/Frontend/Dockerfile`

### 1.3 Запушьте в GitHub

```bash
git add .
git commit -m "Add Render.com deployment config"
git push origin main
```

---

## 🌐 Шаг 2: Создание Web Service (Backend)

### 2.1 Откройте Render Dashboard

1. Перейдите на https://dashboard.render.com
2. Нажмите **"New +"** → **"Web Service"**

### 2.2 Подключите GitHub

1. Выберите **"Build and deploy from a Git repository"**
2. Нажмите **"Connect GitHub"**
3. Авторизуйте Render в GitHub
4. Выберите репозиторий `Designing-intelligent-systems`

### 2.3 Настройте Backend Service

**Basic Settings:**
- **Name:** `sentiment-backend`
- **Region:** Выберите ближайший (Europe/Frankfurt)
- **Branch:** `main`
- **Root Directory:** `Realization/Backend`

**Build Settings:**
- **Runtime:** `Docker`
- **Dockerfile Path:** `Realization/Backend/Dockerfile`

**Advanced Settings:**
- **Instance Type:** `Free` (для начала)
- **Auto-Deploy:** `Yes`

**Environment Variables:**

Добавьте переменные:
```
ENVIRONMENT=production
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

### 2.4 Создайте Service

1. Нажмите **"Create Web Service"**
2. Дождитесь завершения build (~5-10 минут)
3. Скопируйте URL (например: `https://sentiment-backend.onrender.com`)

---

## 📱 Шаг 3: Создание Static Site (Frontend)

### 3.1 Создайте новый Static Site

1. Dashboard → **"New +"** → **"Static Site"**
2. Выберите тот же репозиторий

### 3.2 Настройте Frontend

**Basic Settings:**
- **Name:** `sentiment-frontend`
- **Branch:** `main`
- **Root Directory:** `Realization/Frontend`

**Build Settings:**
- **Build Command:**
  ```bash
  npm install && npm run build
  ```
- **Publish Directory:** `dist`

**Environment Variables:**

```
VITE_API_BASE_URL=https://sentiment-backend.onrender.com
```

⚠️ **Важно:** Замените URL на ваш Backend URL из Шага 2.4

### 3.3 Создайте Static Site

1. Нажмите **"Create Static Site"**
2. Дождитесь build (~3-5 минут)
3. Ваш Frontend будет доступен по URL

---

## 🔧 Шаг 4: Настройка CORS

После деплоя нужно обновить CORS в Backend.

### 4.1 Обновите Backend код

В файле `Realization/Backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sentiment-frontend.onrender.com",  # Ваш Frontend URL
        "http://localhost:5173",  # Для локальной разработки
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4.2 Запушьте изменения

```bash
git add .
git commit -m "Update CORS for Render deployment"
git push origin main
```

Backend автоматически пересоберется.

---

## 📦 Шаг 5: Настройка Persistent Storage (опционально)

Для сохранения моделей между деплоями:

### 5.1 Создайте Disk

1. Dashboard → **"New +"** → **"Disk"**
2. **Name:** `sentiment-models`
3. **Mount Path:** `/data/models`

### 5.2 Присоедините к Backend Service

1. Откройте Backend Service
2. Settings → **"Disks"**
3. **"Add Disk"**
4. Выберите созданный disk

### 5.3 Обновите код для использования

В `config.py`:
```python
MODEL_PATH = Path("/data/models/model.pt")
VOCAB_PATH = Path("/data/models/vocab.json")
```

---

## 🔍 Шаг 6: Проверка работы

### 6.1 Проверьте Backend

```bash
curl https://sentiment-backend.onrender.com/health
```

Ответ:
```json
{
  "model": true,
  "vocab": true,
  "status": "ok"
}
```

### 6.2 Проверьте Frontend

Откройте ваш Frontend URL в браузере:
- https://sentiment-frontend.onrender.com

### 6.3 Проверьте API Docs

- https://sentiment-backend.onrender.com/docs

---

## ⚙️ Шаг 7: Автоматический деплой с render.yaml

Для автоматизации можно использовать Infrastructure as Code.

### 7.1 Используйте Blueprint

1. Dashboard → **"New +"** → **"Blueprint"**
2. Выберите репозиторий
3. Render автоматически найдет `render.yaml`
4. **"Apply"**

Render создаст все сервисы автоматически!

---

## 📊 Мониторинг

### Логи

**Backend:**
1. Dashboard → Backend Service
2. Вкладка **"Logs"**
3. Смотрите в реальном времени

**Frontend:**
1. Dashboard → Frontend Static Site
2. Вкладка **"Logs"**

### Метрики

Render предоставляет:
- CPU usage
- Memory usage
- Response times
- Request count

Доступно в разделе **"Metrics"**

---

## 🔧 Troubleshooting

### Проблема 1: Backend не запускается

**Решение:**
```bash
# Проверьте логи
Dashboard → Backend Service → Logs

# Проверьте health check
curl https://your-backend.onrender.com/health
```

### Проблема 2: Frontend не подключается к Backend

**Проверьте:**
1. ✅ CORS настроен правильно
2. ✅ `VITE_API_BASE_URL` указывает на Backend
3. ✅ Backend запущен и доступен

### Проблема 3: Build fails

**Backend build error:**
```bash
# Проверьте requirements.txt
# Убедитесь, что все зависимости установлены
pip install -r Realization/Backend/requirements.txt
```

**Frontend build error:**
```bash
# Проверьте package.json
# Локально протестируйте build
cd Realization/Frontend
npm run build
```

### Проблема 4: Out of memory

**Free tier ограничения:**
- 512MB RAM для Web Services
- Если не хватает → upgrade на Starter ($7/month)

**Оптимизация:**
```python
# Уменьшите workers в Dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

---

## 💰 Стоимость

### Free Tier

**Включает:**
- ✅ 750 часов/месяц для Web Services
- ✅ Unlimited Static Sites
- ✅ 100GB bandwidth
- ⚠️ Services засыпают после 15 мин неактивности
- ⚠️ 512MB RAM

**Подходит для:**
- Тестирования
- Pet projects
- Демо

### Paid Plans

**Starter ($7/month per service):**
- ✅ Always on
- ✅ 512MB RAM
- ✅ Custom domains

**Standard ($25/month per service):**
- ✅ 2GB RAM
- ✅ Priority support

---

## 🚀 Оптимизация для Production

### 1. Custom Domain

```bash
# В Render Dashboard
Settings → Custom Domains → Add Domain
```

### 2. Environment Variables

Добавьте secrets:
```
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
SENTRY_DSN=your-sentry-dsn
```

### 3. Health Checks

Render автоматически пингует `/health`

Убедитесь, что endpoint работает:
```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

### 4. Auto-scaling

На Starter+ планах:
- Settings → Auto-scaling
- Настройте min/max instances

---

## 📝 Checklist перед деплоем

- [ ] Код запушен в GitHub
- [ ] Dockerfiles проверены локально
- [ ] Environment variables настроены
- [ ] CORS правильно настроен
- [ ] Health checks работают
- [ ] Build тестирован локально
- [ ] Модели загружены (если нужно)

---

## 🔗 Полезные ссылки

- [Render Docs](https://render.com/docs)
- [Render Status](https://status.render.com/)
- [Render Community](https://community.render.com/)
- [Pricing](https://render.com/pricing)

---

## 📞 Поддержка

**Проблемы с деплоем?**

1. Проверьте [DEPLOYMENT.md](DEPLOYMENT.md)
2. Посмотрите логи в Render Dashboard
3. Протестируйте локально с Docker

---

## 🎉 Готово!

После успешного деплоя:

✅ **Backend:** https://sentiment-backend.onrender.com  
✅ **Frontend:** https://sentiment-frontend.onrender.com  
✅ **API Docs:** https://sentiment-backend.onrender.com/docs  

**Поздравляем с деплоем! 🚀**

---

**Обновлено:** 3 декабря 2024  
**Версия:** 1.0

