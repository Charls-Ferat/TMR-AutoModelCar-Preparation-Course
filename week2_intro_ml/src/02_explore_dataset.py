"""
Week 2 - Step 2: load the dataset with the shared CSVImageDataset class
and look at a few (image, label) pairs before training anything.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.dataset import CSVImageDataset, train_val_split

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATASET_DIR = DATA_DIR / "ball_dataset"


def main():
    csv_path = DATASET_DIR / "labels.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} not found. Run 01_make_dataset.py first.")

    dataset = CSVImageDataset(csv_path, DATASET_DIR, label_cols=["target"], image_size=(64, 64))
    print(f"Dataset size: {len(dataset)} samples")

    train_ds, val_ds = train_val_split(dataset, val_ratio=0.2)
    print(f"Train: {len(train_ds)}  Validation: {len(val_ds)}")

    image, label = dataset[0]
    print(f"One sample -> image shape: {tuple(image.shape)}, label: {label.item():.3f}")

    # Preview a 3x3 grid of samples with their labels as titles
    fig, axes = plt.subplots(3, 3, figsize=(6, 6))
    for ax, idx in zip(axes.flat, range(9)):
        image, label = dataset[idx]
        img_hwc = image.permute(1, 2, 0).numpy()  # CHW -> HWC for plotting
        ax.imshow(img_hwc)
        ax.set_title(f"target={label.item():.2f}", fontsize=9)
        ax.axis("off")
    plt.tight_layout()
    out_path = DATA_DIR / "dataset_preview.png"
    plt.savefig(out_path)
    print(f"Saved preview grid -> {out_path}")


if __name__ == "__main__":
    main()
