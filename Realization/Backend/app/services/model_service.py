# app/services/model_service.py
import json
from pathlib import Path
from typing import Optional

# torch импортируем только когда он нужен (позже) — ускоряет импарт модуля сервера
import importlib

from app.config import MODEL_PATH, VOCAB_PATH, CONFIG_PATH
from app.services.utils_service import load_nn_config, tokenize


class ModelService:

    def __init__(self):
        self.model = None
        self.vocab = None
        self.label2id = None
        self.id2label = None
        self.config = load_nn_config(CONFIG_PATH)
        self._torch = None
        # грузим словарь сразу (если есть), модель — лениво
        self._load_vocab()
        self._prepare_labels()

    def _import_torch(self):
        if self._torch is None:
            try:
                import torch as _torch
            except Exception as e:
                raise RuntimeError("Torch не найден в окружении. Установите torch в venv. Ошибка: " + str(e))
            self._torch = _torch
        return self._torch

    def _load_vocab(self):
        if not Path(VOCAB_PATH).exists():
            self.vocab = None
            return
        with open(VOCAB_PATH, "r", encoding="utf-8") as f:
            self.vocab = json.load(f)

    def _prepare_labels(self):
        labels = self.config.get("labels", [])
        self.label2id = {label: i for i, label in enumerate(labels)}
        self.id2label = {i: label for label, i in self.label2id.items()}

    def _ensure_model_loaded(self):
        """Лениво загружает модель (torch + класс модели)"""
        if self.model is not None:
            return

        # провеpка vocab
        if self.vocab is None:
            raise RuntimeError(f"Vocab не найден по пути: {VOCAB_PATH}. Сначала создайте {VOCAB_PATH}")

        torch = self._import_torch()

        # динамический импорт класса модели из пакета app.nn.src.model
        try:
            mod = importlib.import_module("app.nn.src.model")
            BiLSTMAttention = getattr(mod, "BiLSTMAttention")
        except Exception as e:
            raise RuntimeError("Не удалось импортировать класс BiLSTMAttention из app.nn.src.model: " + str(e))

        # создаём модель по конфигу
        self.model = BiLSTMAttention(
            vocab_size=len(self.vocab),
            embedding_dim=self.config["model"]["embedding_dim"],
            hidden_dim=self.config["model"]["hidden_dim"],
            num_layers=self.config["model"]["num_layers"],
            dropout=self.config["model"]["dropout"],
            num_classes=len(self.label2id)
        )

        # загрузка весов
        if not Path(MODEL_PATH).exists():
            # нет модели — оставляем model в памяти, но без весов
            print(f"⚠ Модель отсутствует по пути {MODEL_PATH}. Предсказания невозможны до обучения.")
            return

        try:
            # предпочтительно weights_only=True (безопаснее) — доступно в новых версиях torch
            try:
                state = torch.load(str(MODEL_PATH), map_location="cpu", weights_only=True)
                self.model.load_state_dict(state)
            except TypeError:
                # старый torch — без параметра weights_only
                state = torch.load(str(MODEL_PATH), map_location="cpu")
                self.model.load_state_dict(state)
        except Exception as e:
            raise RuntimeError("Ошибка при загрузке весов модели: " + str(e))

        self.model.eval()
        print("🔧 Модель успешно загружена и готова к предсказаниям.")

    def predict(self, text: str) -> dict:
        """
        Сделать предсказание для текста.
        Возвращает: {"label": "...", "logits": [...], "ok": True/False, "error": "..."}
        """
        try:
            # проверяем словарь и модель
            if self.vocab is None:
                return {"ok": False, "error": f"Vocab не найден по {VOCAB_PATH}"}

            self._ensure_model_loaded()
            if self.model is None:
                return {"ok": False, "error": f"Модель не загружена. Проверьте наличие {MODEL_PATH}"}

            # токенизация
            tokens = tokenize(text)
            token_ids = [self.vocab.get(t, self.vocab.get("<unk>", 0)) for t in tokens]

            max_len = int(self.config["training"]["max_len"])
            token_ids = token_ids[:max_len]
            token_ids += [self.vocab.get("<pad>", 0)] * (max_len - len(token_ids))

            torch = self._import_torch()
            x = torch.tensor([token_ids], dtype=torch.long)

            with torch.no_grad():
                logits = self.model(x)
                probs = torch.softmax(logits, dim=1).squeeze(0).cpu().tolist()
                cls = int(logits.argmax(dim=1).item())
                label = self.id2label.get(cls, "unknown")

            return {"ok": True, "label": label, "probs": probs}
        except Exception as e:
            return {"ok": False, "error": str(e)}


# Singleton/глобальный экземпляр (создаётся при импорте модуля)
loaded_model = ModelService()