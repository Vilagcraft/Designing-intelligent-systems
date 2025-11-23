import torch
import json
from src.model import BiLSTMAttention
from src.utils import tokenize, load_config


def predict_text(text):
    config = load_config()

    vocab = json.load(open(config["paths"]["vocab_path"]))
    label_list = config["labels"]

    model = BiLSTMAttention(
        vocab_size=len(vocab),
        embedding_dim=config["model"]["embedding_dim"],
        hidden_dim=config["model"]["hidden_dim"],
        num_layers=config["model"]["num_layers"],
        dropout=config["model"]["dropout"],
        num_classes=len(label_list)
    )

    model.load_state_dict(torch.load(config["paths"]["model_dir"] + "/model.pt"))
    model.eval()

    tokens = tokenize(text)
    ids = [vocab.get(t, vocab["<unk>"]) for t in tokens]
    ids = ids[:config["training"]["max_len"]]
    ids += [vocab["<pad>"]] * (config["training"]["max_len"] - len(ids))

    x = torch.tensor([ids])
    logits = model(x)
    pred = logits.argmax(dim=1).item()

    return label_list[pred]


if __name__ == "__main__":
    import sys
    text = " ".join(sys.argv[1:])
    print(predict_text(text))