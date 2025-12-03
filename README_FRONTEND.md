# Frontend - Анализ тональности текста

Vue 3 приложение для взаимодействия с сервисом анализа тональности текста.

## Технологии

- **Vue 3** - прогрессивный JavaScript фреймворк
- **Vite** - быстрый инструмент сборки
- **Element Plus** - библиотека UI компонентов
- **Axios** - HTTP клиент для API запросов

## Структура проекта

```
Realization/Frontend/
├── src/
│   ├── api/                    # API клиент
│   │   └── client.js          # Axios конфигурация и методы API
│   ├── components/            # Vue компоненты
│   │   ├── PredictSingle.vue # Анализ одного текста
│   │   ├── PredictBatch.vue  # Batch анализ
│   │   ├── Training.vue      # Управление обучением
│   │   └── SystemHealth.vue  # Статус системы
│   ├── App.vue               # Главный компонент
│   └── main.js               # Точка входа
├── public/                    # Статические файлы
├── index.html                # HTML шаблон
├── vite.config.js            # Конфигурация Vite
└── package.json              # Зависимости и скрипты
```

## Установка

1. Убедитесь, что у вас установлен Node.js 16+ и npm:

```bash
node --version
npm --version
```

2. Перейдите в директорию Frontend:

```bash
cd Realization/Frontend
```

3. Установите зависимости:

```bash
npm install
```

## Запуск

### Development режим

```bash
npm run dev
```

Приложение будет доступно по адресу: http://localhost:5173

### Production сборка

```bash
npm run build
```

Собранные файлы будут находиться в директории `dist/`

### Preview production сборки

```bash
npm run preview
```

## Использование

### Автоматический запуск (Windows)

Используйте батник в корне проекта для запуска Backend и Frontend одновременно:

```bash
start_service.bat
```

### Ручной запуск

1. Запустите Backend сервер:

```bash
cd Realization/Backend
python app/main.py
```

2. В новом терминале запустите Frontend:

```bash
cd Realization/Frontend
npm run dev
```

3. Откройте браузер и перейдите на http://localhost:5173

## Функциональность

### 1. Предсказание тональности

- Анализ одного текста
- Отображение результата с цветовым кодированием
- Показ уровня уверенности модели

### 2. Batch предсказание

- Анализ нескольких текстов одновременно
- Таблица результатов
- Экспорт результатов в JSON

### 3. Обучение модели

- Запуск обучения с настройками
- Опция Force (принудительное переобучение)
- Опция Spark (использование Apache Spark)
- Мониторинг статуса обучения

### 4. Статус системы

- Health check бэкенда
- Проверка наличия модели и словаря
- Скачивание модели и словаря
- Ссылки на API документацию

## API эндпоинты

Backend должен быть доступен на `http://localhost:8000`

- `POST /predict` - анализ одного текста
- `POST /predict/batch` - анализ нескольких текстов
- `POST /train` - запуск обучения
- `GET /train/status` - статус обучения
- `GET /health` - проверка здоровья системы
- `GET /docs` - Swagger документация API

## Конфигурация

### Изменение URL Backend

Отредактируйте `src/api/client.js`:

```javascript
const apiClient = axios.create({
  baseURL: 'http://your-backend-url:port',
  // ...
})
```

### Изменение порта Frontend

Отредактируйте `vite.config.js`:

```javascript
export default defineConfig({
  server: {
    port: 5173, // Измените здесь
    // ...
  }
})
```

## Темная тема

Приложение поддерживает переключение между светлой и темной темой. Кнопка находится в правом верхнем углу. Выбранная тема сохраняется в localStorage.

## Решение проблем

### CORS ошибки

Убедитесь, что Backend настроен с правильными CORS заголовками. В `Realization/Backend/app/main.py` должно быть:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Проблемы с подключением к Backend

1. Убедитесь, что Backend запущен на порту 8000
2. Проверьте URL в `src/api/client.js`
3. Проверьте firewall и антивирус

### Ошибки установки зависимостей

Попробуйте очистить кэш и переустановить:

```bash
rm -rf node_modules package-lock.json
npm install
```

## Лицензия

© 2024 Sentiment Analysis System

