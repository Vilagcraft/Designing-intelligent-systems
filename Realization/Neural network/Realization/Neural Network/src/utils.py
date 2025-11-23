import re
from collections import Counter
import yaml
import json


def tokenize(text):
    text = text.lower()
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ]+", text)


def build_vocab(df, min_freq=3):
    tokens = []

    for t in df["clean_text"]:
        tokens.extend(tokenize(t))

    counter = Counter(tokens)
    vocab = {"<pad>": 0, "<unk>": 1}

    for word, freq in counter.items():
        if freq >= min_freq:
            vocab[word] = len(vocab)

    return vocab


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)