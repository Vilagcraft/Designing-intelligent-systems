import json
import torch
from pathlib import Path

from app.config import MODEL_PATH, VOCAB_PATH, CONFIG_PATH
from app.services.utils_service import load_nn_config, tokenize
from Neural_network.Realization.Neural_Network.src.model import BiLSTMAttention

class ModelService:
    def __init__(self):
        self.model = None
        self.vocab = None
        self.label2id = None
        self.id2label = None
        self.config = load_nn_config(CONFIG_PATH)
        self.load()

    def load(self):
        """Загружаем модель и словарь"""
        if not MODEL_PATH.exists():
            print("⚠ Модель отсутствует, предсказания недоступны.")
            return

        with open(VOCAB_PATH, "r") as f:
            self.vocab = json.load(f)

        labels = self.config["labels"]
        self.label2id = {label: i for i, label in enumerate(labels)}
        self.id2label = {i: label for label, i in self.label2id.items()}

        self.model = BiLSTMAttention(
            vocab_size=len(self.vocab),
            embedding_dim=self.config["model"]["embedding_dim"],
            hidden_dim=self.config["model"]["hidden_dim"],
            num_layers=self.config["model"]["num_layers"],
            dropout=self.config["model"]["dropout"],
            num_classes=len(self.label2id)
        )

        self.model.load_state_dict(torch.load(MODEL_PATH))
        self.model.eval()

        print("🔧 Модель успешно загружена.")

    def predict(self, text: str):
        tokens = tokenize(text)
        token_ids = [self.vocab.get(t, self.vocab["<unk>"]) for t in tokens]

        max_len = self.config["training"]["max_len"]
        token_ids = token_ids[:max_len]
        token_ids += [self.vocab["<pad>"]] * (max_len - len(token_ids))

        x = torch.tensor([token_ids], dtype=torch.long)
        logits = self.model(x)
        cls = logits.argmax(1).item()
        return {"label": self.id2label[cls]}

# глобальный экземпляр модели
loaded_model = ModelService()