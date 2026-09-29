"""
Small, dependency-light helpers for loading and converting images.
Used from Week 1 onwards (OpenCV) and Week 2+ (turning images into
PyTorch tensors for a CNN).
"""

import cv2
import numpy as np


def load_image_bgr(path: str) -> np.ndarray:
    """Load an image from disk in OpenCV's default BGR color order."""
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {path}")
    return img


def bgr_to_rgb(img: np.ndarray) -> np.ndarray:
    """OpenCV loads images as BGR; most other tools (and humans) expect RGB."""
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def resize(img: np.ndarray, size: tuple) -> np.ndarray:
    """Resize an image to (width, height)."""
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def to_tensor(img_bgr: np.ndarray, size: tuple = None):
    """
    Convert a BGR OpenCV image into a normalized PyTorch tensor
    shaped (C, H, W) with values in [0, 1], ready for a CNN.
    """
    import torch  # local import : PyTorch

    if size is not None:
        img_bgr = resize(img_bgr, size)
    img_rgb = bgr_to_rgb(img_bgr)
    img_float = img_rgb.astype(np.float32) / 255.0          # 0..1
    chw = np.transpose(img_float, (2, 0, 1))                 # HWC -> CHW
    return torch.from_numpy(chw.copy())


def overlay_text(img: np.ndarray, text: str, pos=(10, 25)) -> np.ndarray:
    """Draw readable white-on-black text on a frame (handy for debugging)."""
    out = img.copy()
    cv2.putText(out, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(out, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)
    return out
