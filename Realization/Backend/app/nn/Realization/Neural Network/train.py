import json
import torch
import pandas as pd
from pathlib import Path

from src.utils import build_vocab, load_config
from src.dataset import load_dataloaders
from src.model import BiLSTMAttention
from src.trainer import train_model


def full_training_pipeline(config_path="config.yaml"):
    config = load_config(config_path)

    data_path = config["paths"]["data"]
    vocab_path = Path(config["paths"]["vocab_path"])
    model_dir = Path(config["paths"]["model_dir"])

    model_dir.mkdir(parents=True, exist_ok=True)
    vocab_path.parent.mkdir(parents=True, exist_ok=True)

    print("Загружаем датасет…")
    df = pd.read_parquet(data_path)

    print("Строим словарь…")
    vocab = build_vocab(df)

    with open(vocab_path, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

    print(f"Словарь сохранён: {vocab_path}")

    print("Загружаем dataloaders…")
    train_loader, valid_loader, _, label2id = load_dataloaders(config)

    print("Инициализируем модель…")
    model = BiLSTMAttention(
        vocab_size=len(vocab),
        embedding_dim=config["model"]["embedding_dim"],
        hidden_dim=config["model"]["hidden_dim"],
        num_layers=config["model"]["num_layers"],
        dropout=config["model"]["dropout"],
        num_classes=len(label2id)
    )

    print("Начинаем обучение…")
    train_model(model, train_loader, valid_loader, config, vocab)

    print("Обучение завершено!")


if __name__ == "__main__":
    full_training_pipeline("config.yaml")