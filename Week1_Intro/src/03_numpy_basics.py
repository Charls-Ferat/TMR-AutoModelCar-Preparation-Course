import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.image_utils import load_image_bgr

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FRAMES_DIR = DATA_DIR / "frames"
OUT_DIR = DATA_DIR / "numpy_outputs"


def main():
    frame_paths = sorted(FRAMES_DIR.glob("*.jpg"))
    if not frame_paths:
        raise FileNotFoundError(f"No frames in {FRAMES_DIR}. Run 02_extract_frames.py first.")
    OUT_DIR.mkdir(exist_ok=True)

    frame = load_image_bgr(str(frame_paths[len(frame_paths) // 2]))  # a frame from the middle
    print(f"Frame shape: {frame.shape}, dtype: {frame.dtype}")

    # Grayscale by averaging the 3 color channels
    gray = frame.mean(axis=2).astype(np.uint8)
    cv2.imwrite(str(OUT_DIR / "gray_numpy.jpg"), gray)

    # Crop the center half of the frame - array slicing
    h, w = frame.shape[:2]
    crop = frame[h // 4: 3 * h // 4, w // 4: 3 * w // 4]
    cv2.imwrite(str(OUT_DIR / "crop_center.jpg"), crop)

    # 3) Flip left-right using slicing
    flipped = frame[:, ::-1, :]
    cv2.imwrite(str(OUT_DIR / "flipped.jpg"), flipped)

    # 4) Brightness statistics
    left_half = frame[:, : w // 2]
    right_half = frame[:, w // 2:]
    print(f"Mean brightness -> whole: {frame.mean():.1f}, "
          f"left half: {left_half.mean():.1f}, right half: {right_half.mean():.1f}")

    print(f"Saved NumPy exercise outputs -> {OUT_DIR}")


if __name__ == "__main__":
    main()
