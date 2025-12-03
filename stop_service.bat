@echo off
chcp 65001 >nul
cls

echo ====================================
echo   Остановка сервиса
echo ====================================
echo.

echo [*] Остановка Backend сервера (порт 8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo [*] Остановка Frontend сервера (порт 5173)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5173') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo [✓] Все процессы остановлены
echo.
pause

