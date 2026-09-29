"""
Generic training loop, reused from Week 2 onward.
"""

import time
import torch


def train_one_epoch(model, loader, optimizer, loss_fn, device):
    model.train()
    total_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        predictions = model(images)
        loss = loss_fn(predictions, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * images.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, loss_fn, device):
    model.eval()
    total_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        predictions = model(images)
        loss = loss_fn(predictions, labels)
        total_loss += loss.item() * images.size(0)
    return total_loss / len(loader.dataset)


def fit(model, train_loader, val_loader, optimizer, loss_fn, device, epochs, verbose=True):
    """
    Train for `epochs` epochs, printing/recording train & validation loss.
    Returns a history dict: {"train_loss": [...], "val_loss": [...]}.
    """
    model.to(device)
    history = {"train_loss": [], "val_loss": []}

    for epoch in range(1, epochs + 1):
        start = time.time()
        train_loss = train_one_epoch(model, train_loader, optimizer, loss_fn, device)
        val_loss = evaluate(model, val_loader, loss_fn, device)
        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)

        if verbose:
            dt = time.time() - start
            print(f"epoch {epoch:3d}/{epochs} | train_loss {train_loss:.4f} "
                  f"| val_loss {val_loss:.4f} | {dt:.1f}s")

    return history


def plot_history(history, out_path, title="Training curve"):
    """Save a simple train-vs-validation loss plot to `out_path` (PNG)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.figure(figsize=(6, 4))
    plt.plot(history["train_loss"], label="train loss")
    plt.plot(history["val_loss"], label="validation loss")
    plt.xlabel("epoch")
    plt.ylabel("loss")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def count_parameters(model) -> int:
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
