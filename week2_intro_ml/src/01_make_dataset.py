"""
Week 2 - Step 1: build a labeled image dataset.

Reuses Week 1's ball-rendering function (common.python.synthetic_data)
but this time we save every frame straight to disk together with its
true label -- this is the "filename,target" CSV format that
common.python.dataset.CSVImageDataset expects, and that Week 3 reuses
for steering angles.
"""
import csv
import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.synthetic_data import render_ball_frame

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATASET_DIR = DATA_DIR / "ball_dataset"
IMAGE_SIZE = (64, 64)
NUM_SAMPLES = 500


def main():
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)
    csv_path = DATASET_DIR / "labels.csv"

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "target"])
        for i in range(NUM_SAMPLES):
            t = rng.uniform(0, 1)  # random point in the ball's cycle
            frame, x_norm = render_ball_frame(t, size=IMAGE_SIZE)
            filename = f"ball_{i:05d}.jpg"
            cv2.imwrite(str(DATASET_DIR / filename), frame)
            writer.writerow([filename, f"{x_norm:.4f}"])

    print(f"Wrote {NUM_SAMPLES} images + labels -> {DATASET_DIR}")


if __name__ == "__main__":
    main()
