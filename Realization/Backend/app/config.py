from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Путь к нейросети
NN_DIR = BASE_DIR.parent / "Neural network" / "Realization" / "Neural Network"

CONFIG_PATH = NN_DIR / "config.yaml"
MODEL_PATH = NN_DIR / "models" / "model.pt"
VOCAB_PATH = NN_DIR / "models" / "vocab.json"
TRAIN_ENTRY = NN_DIR / "train_entrypoint.py"

# Папка для логов
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Путь к train counter (для каждых 100 запусков)
TRAIN_COUNTER_PATH = NN_DIR / "models" / "train_counter.json"