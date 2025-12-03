@echo off
chcp 65001 >nul
echo ====================================
echo   Установка Backend
echo ====================================
echo.

cd Realization\Backend

REM Создаем виртуальное окружение
if not exist ".venv" (
    echo [*] Создание виртуального окружения...
    python -m venv .venv
)

REM Активируем и устанавливаем зависимости
echo [*] Установка зависимостей...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [✓] Готово!
echo.
echo Для запуска используйте:
echo   start_service.bat
echo.
cd ..\..
pause

