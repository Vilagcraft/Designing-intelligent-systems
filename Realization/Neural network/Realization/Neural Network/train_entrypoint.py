import json
from pathlib import Path

from src.utils import load_config, build_vocab
from src.dataset import load_dataloaders
from src.model import BiLSTMAttention
from src.trainer import train_model
import pandas as pd


def train_entry():
    """
    Отдельный entry-point для обучения.
    Вызывается сервером при первом запуске и потом каждые N запусков.
    """

    print("=== Запуск обучения модели ===")

    config = load_config("config.yaml")

    # 1 — чтение датасета
    print("Загружаем датасет…")
    df = pd.read_parquet(config["paths"]["data"])

    # 2 — словарь
    print("Строим словарь…")
    vocab = build_vocab(df)

    vocab_path = Path(config["paths"]["vocab_path"])
    vocab_path.parent.mkdir(exist_ok=True, parents=True)

    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

    print(f"Словарь сохранён: {vocab_path}")

    # 3 — dataloaders
    print("Загружаем DataLoader’ы…")
    train_loader, valid_loader, _, label2id = load_dataloaders(config)

    # 4 — модель
    print("Инициализируем модель…")
    model = BiLSTMAttention(
        vocab_size=len(vocab),
        embedding_dim=config["model"]["embedding_dim"],
        hidden_dim=config["model"]["hidden_dim"],
        num_layers=config["model"]["num_layers"],
        dropout=config["model"]["dropout"],
        num_classes=len(label2id)
    )

    # 5 — обучение
    print("Начинаем обучение…")
    train_model(model, train_loader, valid_loader, config, vocab)

    print("\n=== Обучение завершено успешно ===")


if __name__ == "__main__":
    train_entry()