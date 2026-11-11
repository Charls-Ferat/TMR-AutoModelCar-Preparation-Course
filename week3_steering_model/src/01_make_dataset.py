"""
Week 3 - Step 1: build the steering dataset.

Unlike Week 2 (where we wrote the dataset-generation loop by hand to
learn how it works), this week's generator is common enough that it
lives in common/python/synthetic_data.py and we just call it -- this is
the "reuse code whenever possible" idea in practice.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.synthetic_data import generate_steering_dataset

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATASET_DIR = DATA_DIR / "steering_dataset"
NUM_SAMPLES = 800


def main():
    csv_path = generate_steering_dataset(DATASET_DIR, num_samples=NUM_SAMPLES, size=(64, 64))
    print(f"Wrote {NUM_SAMPLES} images + labels -> {csv_path}")


if __name__ == "__main__":
    main()
