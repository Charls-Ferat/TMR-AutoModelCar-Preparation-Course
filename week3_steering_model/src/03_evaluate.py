"""
Week 3 - Step 3: evaluate the trained steering model.

A final loss number ("val_loss = 0.01") doesn't tell you much on its
own. This script instead compares predicted vs. actual steering values
directly, the way you should before trusting a model on the real car.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.cnn import SmallCNN
from common.python.dataset import CSVImageDataset, train_val_split

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATASET_DIR = DATA_DIR / "steering_dataset"
MODEL_PATH = DATA_DIR / "steering_cnn.pt"
IMAGE_SIZE = (64, 64)


def main():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"{MODEL_PATH} not found. Run 02_train.py first.")

    dataset = CSVImageDataset(DATASET_DIR / "labels.csv", DATASET_DIR,
                               label_cols=["steering"], image_size=IMAGE_SIZE)
    # Same split settings as training, so this is the held-out validation set
    _, val_ds = train_val_split(dataset, val_ratio=0.2)
    val_loader = DataLoader(val_ds, batch_size=32)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SmallCNN(in_channels=3, out_features=1, image_size=IMAGE_SIZE[0])
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()

    actuals, predictions = [], []
    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(device)
            preds = model(images).cpu().numpy().flatten()
            predictions.extend(preds.tolist())
            actuals.extend(labels.numpy().flatten().tolist())

    actuals = np.array(actuals)
    predictions = np.array(predictions)
    errors = predictions - actuals

    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors ** 2))
    max_err = np.max(np.abs(errors))
    print(f"Validation samples: {len(actuals)}")
    print(f"MAE:  {mae:.4f}")
    print(f"RMSE: {rmse:.4f}")
    print(f"Max absolute error: {max_err:.4f}")

    worst_idx = np.argsort(-np.abs(errors))[:5]
    print("5 worst predictions (index, actual, predicted, abs error):")
    for i in worst_idx:
        print(f"  {i:4d}  actual={actuals[i]:+.3f}  predicted={predictions[i]:+.3f}  "
              f"error={abs(errors[i]):.3f}")

    # Predicted vs actual scatter plot -- points on the diagonal = perfect
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    axes[0].scatter(actuals, predictions, s=12, alpha=0.6)
    lims = [-1.05, 1.05]
    axes[0].plot(lims, lims, "r--", linewidth=1, label="perfect prediction")
    axes[0].set_xlabel("actual steering")
    axes[0].set_ylabel("predicted steering")
    axes[0].set_title("Predicted vs. actual")
    axes[0].legend()
    axes[0].set_xlim(lims)
    axes[0].set_ylim(lims)

    axes[1].plot(np.abs(errors), marker=".", linestyle="none")
    axes[1].axhline(mae, color="r", linestyle="--", label=f"MAE = {mae:.3f}")
    axes[1].set_xlabel("validation sample index")
    axes[1].set_ylabel("absolute error")
    axes[1].set_title("Error per sample")
    axes[1].legend()

    plt.tight_layout()
    out_path = DATA_DIR / "evaluation.png"
    plt.savefig(out_path)
    print(f"Saved evaluation plots -> {out_path}")


if __name__ == "__main__":
    main()
