import yaml
import re

def load_nn_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

TOKEN_RE = re.compile(r"[а-яa-z0-9]+", re.IGNORECASE)

def tokenize(text: str):
    return TOKEN_RE.findall(text.lower())