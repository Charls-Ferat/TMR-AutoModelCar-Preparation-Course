"""
Week 2 - Step 4: deliberately overfit.

The ball-position task is *too easy* to overfit just by shrinking the
dataset (the CNN generalizes fine even from very few images, because
"find the bright blob" is a simple, smooth pattern). So instead we do
what real overfitting looks like: give the model a tiny training set
with a bit of **label noise** it can only get right by memorizing.

Watch `data/overfit_loss.png`: train loss keeps dropping (the model is
memorizing the noisy training labels) while validation loss stalls or
gets worse (memorized noise doesn't generalize) -- that gap *is*
overfitting.
"""
import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.cnn import SmallCNN
from common.python.dataset import CSVImageDataset, train_val_split
from common.python.train_utils import fit, plot_history

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATASET_DIR = DATA_DIR / "ball_dataset"
IMAGE_SIZE = (64, 64)
TINY_TRAIN_SIZE = 12    # deliberately small -> easy to memorize
LABEL_NOISE_STD = 0.35  # each training label gets a fixed random offset
EPOCHS = 60


class NoisyLabelDataset(Dataset):
    """
    Wraps another dataset and adds a fixed random offset to each label.
    The offset is the same every epoch, so the network can only reduce
    training loss further by memorizing each individual noisy label --
    exactly the behaviour we want to demonstrate.
    """

    def __init__(self, base_dataset, num_samples, noise_std, seed=1):
        self.base = base_dataset
        self.indices = list(range(min(num_samples, len(base_dataset))))
        rng = np.random.default_rng(seed)
        self.noise = {i: rng.normal(0.0, noise_std) for i in self.indices}

    def __len__(self):
        return len(self.indices)

    def __getitem__(self, i):
        image, label = self.base[self.indices[i]]
        noisy_label = label + self.noise[self.indices[i]]
        return image, noisy_label.float()


def main():
    csv_path = DATASET_DIR / "labels.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} not found. Run 01_make_dataset.py first.")

    dataset = CSVImageDataset(csv_path, DATASET_DIR, label_cols=["target"], image_size=IMAGE_SIZE)
    train_ds, val_ds = train_val_split(dataset, val_ratio=0.3)  # val_ds keeps clean labels

    tiny_noisy_train_ds = NoisyLabelDataset(train_ds, TINY_TRAIN_SIZE, LABEL_NOISE_STD)
    train_loader = DataLoader(tiny_noisy_train_ds, batch_size=4, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=32)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SmallCNN(in_channels=3, out_features=1, image_size=IMAGE_SIZE[0])
    optimizer = torch.optim.Adam(model.parameters(), lr=2e-3)  # try adding weight_decay=1e-4
    loss_fn = torch.nn.MSELoss()

    print(f"Training on {len(tiny_noisy_train_ds)} images with noisy labels "
          f"for {EPOCHS} epochs...")
    history = fit(model, train_loader, val_loader, optimizer, loss_fn, device, EPOCHS)

    plot_path = DATA_DIR / "overfit_loss.png"
    plot_history(history, plot_path, title="Overfitting demo (tiny + noisy labels)")
    print(f"Saved overfitting loss curve -> {plot_path}")
    print("Look at the plot: train loss keeps dropping (memorizing noise), "
          "validation loss stalls or rises.")


if __name__ == "__main__":
    main()
