import os
import subprocess
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Абсолютные импорты! (решает ошибку ImportError)
from app.router_predict import router as predict_router
from app.router_train import router as train_router
from app.router_system import router as system_router


# ============================================================
# 1. Автоматическая проверка venv + установка зависимостей
# ============================================================

def ensure_venv_and_dependencies():

    # Если уже внутри venv — всё ок
    if sys.prefix != sys.base_prefix:
        return

    print("⚙️  Автоматическая настройка окружения...")

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    venv_path = os.path.join(project_root, ".venv")

    # Создание venv
    if not os.path.exists(venv_path):
        print("📦 Создаём виртуальное окружение...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])

    pip_exec = os.path.join(venv_path, "bin", "pip")
    python_exec = os.path.join(venv_path, "bin", "python")

    # Установка зависимостей
    req_file = os.path.join(project_root, "requirements.txt")
    print("📥 Устанавливаем зависимости...")
    subprocess.check_call([pip_exec, "install", "-r", req_file])

    print("✅ Окружение готово.")

    print("🔄 Перезапуск внутри виртуального окружения...")
    os.execv(python_exec, [python_exec, __file__])


# Запуск автопроверки
ensure_venv_and_dependencies()


# ============================================================
# 2. FastAPI приложение
# ============================================================

app = FastAPI(title="Sentiment Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system_router)
app.include_router(predict_router)
app.include_router(train_router)


# ============================================================
# 3. Автозапуск Uvicorn при RUN в PyCharm
# ============================================================

def run_server():
    if __name__ == "__main__":
        print("🚀 Запуск API-сервера...")
        import uvicorn
        uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


run_server()


# ============================================================
# Корневой маршрут
# ============================================================

@app.get("/")
def root():
    return {"status": "backend running"}