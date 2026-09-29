"""
Generic PyTorch Dataset (Week 2 onward): it reads a folder
of images plus a `labels.csv` file with a `filename` column and one or
more numeric label columns.
"""

import csv
import os

from torch.utils.data import Dataset, random_split
from .image_utils import load_image_bgr, to_tensor


class CSVImageDataset(Dataset):
    """
    Args:
        csv_path:   path to a CSV file with a 'filename' column and one
                    or more numeric label columns.
        img_dir:    folder containing the images referenced by 'filename'.
        label_cols: list of column names to use as the label, e.g.
                    ['steering']. If there is one column, the label is a
                    single float; if more, a small vector.
        image_size: (width, height) to resize every image to.
    """

    def __init__(self, csv_path, img_dir, label_cols=("target",), image_size=(64, 64)):
        self.img_dir = img_dir
        self.label_cols = list(label_cols)
        self.image_size = image_size
        self.rows = []

        with open(csv_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.rows.append(row)

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, idx):
        row = self.rows[idx]
        img_path = os.path.join(self.img_dir, row["filename"])
        image = load_image_bgr(img_path)
        image_tensor = to_tensor(image, size=self.image_size)

        import torch
        label_values = [float(row[col]) for col in self.label_cols]
        label_tensor = torch.tensor(label_values, dtype=torch.float32)
        return image_tensor, label_tensor


def train_val_split(dataset, val_ratio: float = 0.2, seed: int = 42):
    """Randomly split a dataset into (train_dataset, val_dataset)."""
    import torch

    n_val = int(len(dataset) * val_ratio)
    n_train = len(dataset) - n_val
    generator = torch.Generator().manual_seed(seed)
    return random_split(dataset, [n_train, n_val], generator=generator)
