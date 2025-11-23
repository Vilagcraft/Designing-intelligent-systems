import argparse
from predict import predict_text
from train import train_model
from evaluate import evaluate_model

def main():
    parser = argparse.ArgumentParser(description="Neural Network Module")

    parser.add_argument("--mode", type=str, required=True,
                        choices=["train", "predict", "evaluate"],
                        help="Режим работы модуля")

    parser.add_argument("--text", type=str,
                        help="Текст для предсказания (mode=predict)")
    parser.add_argument("--config", type=str, default="config.yaml",
                        help="Путь к YAML конфигурации")

    args = parser.parse_args()

    if args.mode == "train":
        train_model(args.config)

    elif args.mode == "predict":
        if not args.text:
            raise ValueError("В режиме predict необходимо передать --text")
        result = predict_text(args.text, args.config)
        print(result)

    elif args.mode == "evaluate":
        evaluate_model(args.config)

if __name__ == "__main__":
    main()