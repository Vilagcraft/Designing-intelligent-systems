# ⚡ Быстрый старт на Render.com

## За 5 минут к деплою! 🚀

---

## 1️⃣ Подготовка (2 минуты)

```bash
# Убедитесь, что код в GitHub
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

---

## 2️⃣ Backend (2 минуты)

1. Откройте https://dashboard.render.com
2. **New +** → **Web Service**
3. Подключите GitHub → выберите репозиторий
4. Настройте:
   ```
   Name: sentiment-backend
   Runtime: Docker
   Root Directory: Realization/Backend
   Dockerfile Path: Realization/Backend/Dockerfile
   Instance Type: Free
   ```
5. **Create Web Service**
6. Скопируйте URL (нужен для следующего шага)

---

## 3️⃣ Frontend (1 минута)

1. **New +** → **Static Site**
2. Выберите тот же репозиторий
3. Настройте:
   ```
   Name: sentiment-frontend
   Root Directory: Realization/Frontend
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```
4. Environment Variables:
   ```
   VITE_API_BASE_URL=https://sentiment-backend.onrender.com
   ```
   ⚠️ Замените на ваш Backend URL!
5. **Create Static Site**

---

## 4️⃣ Проверка (30 секунд)

Откройте в браузере:
- Frontend: `https://sentiment-frontend.onrender.com`
- Backend API: `https://sentiment-backend.onrender.com/docs`

---

## 🎉 Готово!

Система задеплоена и работает!

---

## 🔧 Если что-то не работает:

### CORS ошибка?

Обновите `Realization/Backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://sentiment-frontend.onrender.com",  # ← Ваш URL
    ],
    # ...
)
```

Запушьте:
```bash
git add .
git commit -m "Fix CORS"
git push origin main
```

Backend пересоберется автоматически!

---

### Build failed?

Проверьте логи:
- Dashboard → Service → Logs

---

### Free tier засыпает?

Это нормально на Free плане.  
Upgrade на Starter ($7/month) для always-on.

---

## 📚 Подробнее:

См. [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

---

**Успехов! 🚀**

