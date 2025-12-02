import torch
import json
from src.model import BiLSTMAttention
from src.utils import tokenize, load_config


def predict_text(text, config_path="config.yaml"):
    import json
    import torch
    from src.utils import load_config, tokenize
    from src.model import BiLSTMAttention

    # load config
    config = load_config(config_path)

    # load vocab
    with open(config["paths"]["vocab_path"], "r", encoding="utf-8") as f:
        vocab = json.load(f)

    # inverse label mapping
    id2label = {i: label for i, label in enumerate(config["labels"])}

    # load model
    model = BiLSTMAttention(
        vocab_size=len(vocab),
        embedding_dim=config["model"]["embedding_dim"],
        hidden_dim=config["model"]["hidden_dim"],
        num_layers=config["model"]["num_layers"],
        dropout=config["model"]["dropout"],
        num_classes=len(config["labels"]),
    )

    model.load_state_dict(torch.load(config["paths"]["model_dir"] + "/model.pt"))
    model.eval()

    # preprocess
    tokens = tokenize(text)
    token_ids = [vocab.get(t, vocab["<unk>"]) for t in tokens]
    token_ids = token_ids[:config["training"]["max_len"]]
    token_ids += [vocab["<pad>"]] * (config["training"]["max_len"] - len(token_ids))

    x = torch.tensor([token_ids])

    with torch.no_grad():
        logits = model(x)
        pred = logits.argmax(dim=1).item()

    return id2label[pred]


if __name__ == "__main__":
    import sys
    text = " ".join(sys.argv[1:])
    print(predict_text(text))