import json
import torch
import pandas as pd
from pathlib import Path
from src.utils import build_vocab, load_config
from src.dataset import load_dataloaders
from src.model import BiLSTMAttention
from src.trainer import train_model


if __name__ == "__main__":
    config = load_config("config.yaml")

    # подготовка словаря
    df = pd.read_parquet(config["paths"]["data"])
    vocab = build_vocab(df)

    with open(config["paths"]["vocab_path"], "w") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

    # dataloaders
    train_loader, valid_loader, _, label2id = load_dataloaders(config)

    model = BiLSTMAttention(
        vocab_size=len(vocab),
        embedding_dim=config["model"]["embedding_dim"],
        hidden_dim=config["model"]["hidden_dim"],
        num_layers=config["model"]["num_layers"],
        dropout=config["model"]["dropout"],
        num_classes=len(label2id)
    )

    train_model(model, train_loader, valid_loader, config, vocab)