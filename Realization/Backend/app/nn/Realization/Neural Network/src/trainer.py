import torch
import torch.nn as nn
from tqdm import tqdm
from pathlib import Path
import json
from .utils import build_vocab, load_config


def train_model(model, train_loader, valid_loader, config, vocab):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=config["training"]["lr"])
    criterion = nn.CrossEntropyLoss()

    # сохраняем словарь
    Path(config["paths"]["model_dir"]).mkdir(exist_ok=True)
    with open(config["paths"]["vocab_path"], "w") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)

    for epoch in range(config["training"]["num_epochs"]):
        model.train()
        total_loss = 0

        for batch in tqdm(train_loader, desc=f"Training epoch {epoch+1}"):
            x, y = batch
            x, y = x.to(device), y.to(device)

            optimizer.zero_grad()
            logits = model(x)
            loss = criterion(logits, y)
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}: loss = {total_loss / len(train_loader):.4f}")

    torch.save(model.state_dict(), config["paths"]["model_dir"] + "/model.pt")
    print("Модель сохранена!")