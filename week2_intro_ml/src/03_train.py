"""
Week 2 - Step 3: train a small CNN to predict the ball's position from
its image. This is the same train/evaluate/plot code Week 3 reuses for
steering prediction and Week 4 reuses on GPU.
"""
import sys
from pathlib import Path

import torch
from torch.utils.data import DataLoader

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.cnn import SmallCNN
from common.python.dataset import CSVImageDataset, train_val_split
from common.python.train_utils import fit, plot_history, count_parameters

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATASET_DIR = DATA_DIR / "ball_dataset"
IMAGE_SIZE = (64, 64)
EPOCHS = 15
BATCH_SIZE = 32
LEARNING_RATE = 1e-3


def main():
    csv_path = DATASET_DIR / "labels.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} not found. Run 01_make_dataset.py first.")

    dataset = CSVImageDataset(csv_path, DATASET_DIR, label_cols=["target"], image_size=IMAGE_SIZE)
    train_ds, val_ds = train_val_split(dataset, val_ratio=0.2)
    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Training on: {device}")

    model = SmallCNN(in_channels=3, out_features=1, image_size=IMAGE_SIZE[0])
    print(f"Model has {count_parameters(model):,} trainable parameters")

    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    loss_fn = torch.nn.MSELoss()

    history = fit(model, train_loader, val_loader, optimizer, loss_fn, device, EPOCHS)

    plot_path = DATA_DIR / "training_loss.png"
    plot_history(history, plot_path, title="Week 2: ball position CNN")
    print(f"Saved loss curve -> {plot_path}")

    model_path = DATA_DIR / "ball_cnn.pt"
    torch.save(model.state_dict(), model_path)
    print(f"Saved trained model -> {model_path}")


if __name__ == "__main__":
    main()
