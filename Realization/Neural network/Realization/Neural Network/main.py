import json
from pathlib import Path

from src.utils import load_config
from predict import predict_text
from evaluate import evaluate_model


def main():
    """
    Основной запуск нейросети:
    - предсказания
    - оценка
    (без обучения)
    """

    print("=== Запуск inference & evaluation ===\n")

    config = load_config("config.yaml")

    # загрузка словаря
    vocab_path = Path(config["paths"]["vocab_path"])
    if not vocab_path.exists():
        raise FileNotFoundError(
            f"Словарь не найден: {vocab_path}\n"
            f"Сначала запустите обучение:\n"
            f"    python train_entrypoint.py"
        )

    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab = json.load(f)

    print("Словарь загружен.")

    # тестовые примеры
    print("\nТестовые предсказания:")
    examples = [
        "Отличный товар, рекомендую!",
        "Ужасное качество, никогда больше!",
        "Всё нормально."
    ]

    for text in examples:
        pred = predict_text(text, "config.yaml")
        print(f" → «{text}» → {pred}")

    print("\nОцениваем качество модели...")
    evaluate_model("config.yaml")

    print("\nГотово.")


if __name__ == "__main__":
    main()