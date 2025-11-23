import torch
import json
from sklearn.metrics import classification_report
from src.model import BiLSTMAttention
from src.dataset import load_dataloaders
from src.utils import load_config


def evaluate_model(config_path="config.yaml"):
    config = load_config(config_path)

    _, _, test_loader, label2id = load_dataloaders(config)
    id2label = {v: k for k, v in label2id.items()}

    # Загружаем словарь
    with open(config["paths"]["vocab_path"], "r", encoding="utf-8") as f:
        vocab = json.load(f)

    # Создаём модель
    model = BiLSTMAttention(
        vocab_size=len(vocab),
        embedding_dim=config["model"]["embedding_dim"],
        hidden_dim=config["model"]["hidden_dim"],
        num_layers=config["model"]["num_layers"],
        dropout=config["model"]["dropout"],
        num_classes=len(label2id)
    )

    # Загружаем веса
    model.load_state_dict(torch.load(config["paths"]["model_dir"] + "/model.pt"))
    model.eval()

    all_preds, all_labels = [], []

    for x, y in test_loader:
        logits = model(x)
        preds = logits.argmax(dim=1).tolist()
        labels = y.tolist()
        all_preds.extend(preds)
        all_labels.extend(labels)

    report = classification_report(
        all_labels,
        all_preds,
        target_names=list(id2label.values())
    )

    print(report)
    return report


if __name__ == "__main__":
    evaluate_model()