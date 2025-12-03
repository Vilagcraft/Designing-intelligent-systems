import subprocess
import threading
import time

from app.config import TRAIN_ENTRY, LOGS_DIR

TRAIN_STATUS = {
    "running": False,
    "last_run": None,
    "result": None,
    "pid": None
}

def _run_training(use_spark: bool):
    try:
        import sys
        import os
        
        # Проверяем существование файла обучения
        if not TRAIN_ENTRY.exists():
            raise FileNotFoundError(f"Training script not found: {TRAIN_ENTRY}")
        
        cmd = []
        
        if use_spark:
            cmd = ["spark-submit", str(TRAIN_ENTRY)]
        else:
            # Используем текущий Python interpreter (работает на Windows и Linux)
            python_exe = sys.executable
            cmd = [python_exe, str(TRAIN_ENTRY)]

        logfile = LOGS_DIR / f"train_{int(time.time())}.log"
        
        # Создаем логи директорию если не существует
        LOGS_DIR.mkdir(exist_ok=True)

        with open(logfile, "w", encoding="utf-8") as f:
            # Добавляем переменные окружения для правильных путей
            env = os.environ.copy()
            env["PYTHONPATH"] = str(TRAIN_ENTRY.parent.parent.parent)
            
            p = subprocess.Popen(
                cmd, 
                stdout=f, 
                stderr=f,
                env=env,
                cwd=str(TRAIN_ENTRY.parent)  # Запускаем из директории скрипта
            )
            TRAIN_STATUS["pid"] = p.pid
            returncode = p.wait()
            
            if returncode != 0:
                TRAIN_STATUS["result"] = f"error: Training exited with code {returncode}. Check logs: {logfile}"
            else:
                TRAIN_STATUS["result"] = f"success: Training completed. Logs: {logfile}"

        TRAIN_STATUS["running"] = False
        TRAIN_STATUS["last_run"] = time.ctime()
    except Exception as e:
        TRAIN_STATUS["result"] = f"error: {e}"
        TRAIN_STATUS["running"] = False
        TRAIN_STATUS["last_run"] = time.ctime()

def start_training(force: bool = False, use_spark: bool = False):
    if TRAIN_STATUS["running"]:
        return {"status": "Already running"}

    TRAIN_STATUS["running"] = True
    TRAIN_STATUS["result"] = None
    t = threading.Thread(target=_run_training, args=(use_spark,), daemon=True)
    t.start()

    return {"status": "training started"}

def get_train_status():
    return TRAIN_STATUS