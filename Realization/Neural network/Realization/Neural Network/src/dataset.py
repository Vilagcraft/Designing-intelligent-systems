import torch
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import json
from pathlib import Path
from .utils import tokenize


class ReviewsDataset(Dataset):
    def __init__(self, df, vocab, max_len, label2id):
        self.texts = df["clean_text"].tolist()
        self.labels = df["rating"].map(label2id).tolist()
        self.vocab = vocab
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        tokens = tokenize(text)

        token_ids = [self.vocab.get(t, self.vocab["<unk>"]) for t in tokens]

        # pad / truncate
        token_ids = token_ids[: self.max_len]
        token_ids += [self.vocab["<pad>"]] * (self.max_len - len(token_ids))

        return torch.tensor(token_ids), torch.tensor(label)


def load_dataloaders(config):
    df = pd.read_parquet(config["paths"]["data"])

    # Маппинг классов
    labels = config["labels"]
    label2id = {label: i for i, label in enumerate(labels)}

    # Разделение 80/10/10
    train_df = df.sample(frac=0.8, random_state=42)
    temp = df.drop(train_df.index)
    valid_df = temp.sample(frac=0.5, random_state=42)
    test_df = temp.drop(valid_df.index)

    # загружаем словарь
    vocab_path = Path(config["paths"]["vocab_path"])
    vocab = json.load(open(vocab_path)) if vocab_path.exists() else {}

    train_dataset = ReviewsDataset(train_df, vocab, config["training"]["max_len"], label2id)
    valid_dataset = ReviewsDataset(valid_df, vocab, config["training"]["max_len"], label2id)
    test_dataset = ReviewsDataset(test_df, vocab, config["training"]["max_len"], label2id)

    return (
        DataLoader(train_dataset, batch_size=config["training"]["batch_size"], shuffle=True),
        DataLoader(valid_dataset, batch_size=config["training"]["batch_size"]),
        DataLoader(test_dataset, batch_size=config["training"]["batch_size"]),
        label2id
    )