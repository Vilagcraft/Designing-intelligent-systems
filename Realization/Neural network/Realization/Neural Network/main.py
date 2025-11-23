import json
import os
import torch

from src.utils import load_config
from src.dataset import load_dataloaders
from train import train_model
from predict import predict_text
from evaluate import evaluate_model


def auto_run():
    """
    Автоматический end-to-end запуск:
    1. Загрузка конфига
    2. Загрузка датасета
    3. Обучение модели
    4. Предсказание примеров
    5. Оценка качества модели
    """
    print("Запуск полного ML-конвейера (обучение → предсказание → оценка)")

    # 1. Load config
    print("Загружаем конфигурацию…")
    config = load_config("config.yaml")

    # 2. Load data
    print("Загружаем датасеты…")
    train_loader, valid_loader, test_loader, label2id = load_dataloaders(config)

    # Load vocabulary
    print("Загружаем словарь…")
    vocab_path = config["paths"]["vocab_path"]
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab = json.load(f)

    # 3. Train the model
    print("Начинаем обучение модели…")
    train_model(train_loader, valid_loader, config, vocab)

    # 4. Run predictions
    print("\nТестовое предсказание:")
    test_examples = [
        "Отличный товар, рекомендую!",
        "Ужасное качество, больше не куплю.",
        "Обычный товар, ничего особенного."
    ]

    for text in test_examples:
        pred = predict_text(text, "config.yaml")
        print(f" → {text}  →  {pred}")

    # 5. Evaluate model quality
    print("\nОцениваем качество модели…")
    evaluate_model("config.yaml")

    print("\nПолный цикл успешно завершён.")


if __name__ == "__main__":
    auto_run()