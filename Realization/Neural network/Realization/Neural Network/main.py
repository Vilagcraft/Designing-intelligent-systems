import json
from pathlib import Path

from src.utils import load_config
from src.dataset import load_dataloaders
from train import full_training_pipeline
from predict import predict_text
from evaluate import evaluate_model


COUNTER_FILE = Path("models/train_counter.json")


def should_train() -> bool:
    """
    Возвращает True, если нужно запустить обучение:
    - модель ещё не обучалась (counter.json нет)
    - счётчик запусков кратен 100
    """

    if not COUNTER_FILE.exists():
        print("Счётчик запусков отсутствует — создаём новый и запускаем обучение.")
        return True

    with open(COUNTER_FILE, "r") as f:
        data = json.load(f)

    runs = data.get("runs", 0)

    # обучать, если запуск № 100, 200, ...
    return runs % 100 == 0


def increment_counter():
    """Увеличивает счётчик запусков."""
    if not COUNTER_FILE.exists():
        data = {"runs": 1}
    else:
        data = json.load(open(COUNTER_FILE))
        data["runs"] += 1

    with open(COUNTER_FILE, "w") as f:
        json.dump(data, f, indent=2)


def auto_run():
    print("Запуск полного ML-конвейера (train → predict → evaluate)\n")

    config = load_config("config.yaml")

    # 0. Увеличиваем счётчик
    increment_counter()

    # 1. Решаем — нужно ли обучать модель
    if should_train():
        print("\nУсловие обучения выполнено — запускаем обучение.")
        full_training_pipeline("config.yaml")
    else:
        print("\nОбучение пропущено (до следующего цикла из 100 запусков).")

    # 2. Предсказания
    print("\nЗагружаем словарь…")
    vocab_path = Path(config["paths"]["vocab_path"])
    with open(vocab_path, "r", encoding="utf-8") as f:
        vocab = json.load(f)

    print("\nТестовые предсказания:")
    examples = [
        "Отличный товар, рекомендую!",
        "Ужасное качество, больше не куплю.",
        "Обычный товар, ничего особенного."
    ]

    for text in examples:
        pred = predict_text(text)
        print(f" → «{text}»  →  {pred}")

    # 3. Оценка
    print("\nОцениваем качество модели…")
    evaluate_model("config.yaml")

    print("\nПолный ML-процесс завершён успешно!")


if __name__ == "__main__":
    auto_run()