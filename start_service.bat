@echo off
chcp 65001 >nul
cls

echo ====================================
echo   Запуск сервиса анализа тональности
echo ====================================
echo.

REM Проверяем наличие Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Python не найден!
    echo Установите Python 3.8+ и добавьте его в PATH
    pause
    exit /b 1
)

REM Проверяем наличие Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ОШИБКА] Node.js не найден!
    echo Установите Node.js 16+ и добавьте его в PATH
    pause
    exit /b 1
)

echo [✓] Python установлен
echo [✓] Node.js установлен
echo.

REM Проверяем и устанавливаем зависимости для Frontend
echo ====================================
echo   Настройка Frontend
echo ====================================
if not exist "Realization\Frontend\node_modules" (
    echo [!] node_modules не найдены
    echo [*] Устанавливаем зависимости...
    cd Realization\Frontend
    call npm install
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось установить зависимости Frontend
        cd ..\..
        pause
        exit /b 1
    )
    cd ..\..
    echo [✓] Зависимости Frontend установлены
) else (
    echo [✓] Зависимости Frontend уже установлены
)
echo.

REM Проверяем и настраиваем Backend
echo ====================================
echo   Настройка Backend
echo ====================================
if not exist "Realization\Backend\.venv" (
    echo [!] Виртуальное окружение не найдено
    echo [*] Создание виртуального окружения...
    cd Realization\Backend
    python -m venv .venv
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось создать виртуальное окружение
        cd ..\..
        pause
        exit /b 1
    )
    echo [*] Установка зависимостей...
    call .venv\Scripts\activate.bat
    python -m pip install --upgrade pip >nul 2>&1
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ОШИБКА] Не удалось установить зависимости Backend
        cd ..\..
        pause
        exit /b 1
    )
    cd ..\..
    echo [✓] Backend настроен успешно
) else (
    echo [✓] Виртуальное окружение найдено
    echo [*] Проверка и обновление зависимостей...
    cd Realization\Backend
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt --quiet
    cd ..\..
    echo [✓] Зависимости проверены
)
echo.

echo ====================================
echo   Запуск сервисов
echo ====================================
echo.

REM Запускаем Backend в отдельном окне
echo [1/2] Запуск Backend сервера...
start "Backend Server - Sentiment Analysis" cmd /k "cd /d %CD%\Realization\Backend && .venv\Scripts\activate.bat && python app\main.py"

REM Ждем немного, чтобы Backend успел запуститься
echo [*] Ожидание запуска Backend (5 секунд)...
timeout /t 5 /nobreak >nul

REM Запускаем Frontend в отдельном окне
echo [2/2] Запуск Frontend сервера...
start "Frontend Dev Server - Sentiment Analysis" cmd /k "cd /d %CD%\Realization\Frontend && npm run dev"

echo.
echo ====================================
echo   Сервис запущен!
echo ====================================
echo.
echo [Backend]  http://localhost:8000
echo [API Docs] http://localhost:8000/docs
echo [Frontend] http://localhost:5173
echo.
echo Два окна терминала были открыты:
echo - Backend Server (Python/FastAPI)
echo - Frontend Dev Server (Vue/Vite)
echo.
echo Для остановки закройте оба окна или нажмите Ctrl+C в каждом
echo.
echo Откройте браузер и перейдите на http://localhost:5173
echo.
pause

