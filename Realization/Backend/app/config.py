from pathlib import Path

# === Корень проекта (Backend) ===
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# === Путь к нейросети (внутри app/nn/...) ===
NN_ROOT = PROJECT_ROOT / "app" / "nn" / "Realization" / "Neural Network"

# === Пути к файлам нейросети ===
CONFIG_PATH = NN_ROOT / "config.yaml"
MODEL_PATH = NN_ROOT / "models" / "model.pt"
VOCAB_PATH = NN_ROOT / "models" / "vocab.json"
TRAIN_COUNTER_PATH = NN_ROOT / "models" / "train_counter.json"

# Путь к train_entrypoint.py (файл для запуска обучения)
TRAIN_ENTRY = NN_ROOT / "train_entrypoint.py"

# === Папка логов сервера ===
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Опциональная проверка
def assert_nn_paths_exist(raise_on_missing: bool = False):
    missing = [p for p in (CONFIG_PATH, MODEL_PATH.parent) if not p.exists()]
    if missing and raise_on_missing:
        raise FileNotFoundError(f"NN files missing: {missing}")
    return missing