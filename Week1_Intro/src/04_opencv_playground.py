"""
Week 1 - Step 4: common OpenCV operations you'll reuse when preprocessing
camera images for the TMR car: color conversion, blurring, edge
detection, and drawing overlays.
"""
import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.image_utils import load_image_bgr, overlay_text

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FRAMES_DIR = DATA_DIR / "frames"
OUT_DIR = DATA_DIR / "opencv_outputs"


def main():
    frame_paths = sorted(FRAMES_DIR.glob("*.jpg"))
    if not frame_paths:
        raise FileNotFoundError(f"No frames in {FRAMES_DIR}. Run 02_extract_frames.py first.")
    OUT_DIR.mkdir(exist_ok=True)

    frame = load_image_bgr(str(frame_paths[len(frame_paths) // 2]))

    # Color space conversion
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imwrite(str(OUT_DIR / "hsv.jpg"), hsv)

    # Blurring 
    blurred = cv2.GaussianBlur(frame, (5, 5), sigmaX=0)
    cv2.imwrite(str(OUT_DIR / "blurred.jpg"), blurred)

    # Edge detection 
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=60, threshold2=150)
    cv2.imwrite(str(OUT_DIR / "edges.jpg"), edges)

    # Drawing overlays: a rectangle, a circle, and text 
    annotated = frame.copy()
    h, w = annotated.shape[:2]
    cv2.rectangle(annotated, (10, 10), (w - 10, h - 10), (0, 255, 0), 2)
    cv2.circle(annotated, (w // 2, h // 2), 15, (0, 0, 255), 2)
    annotated = overlay_text(annotated, "Nananana")
    cv2.imwrite(str(OUT_DIR / "annotated.jpg"), annotated)

    print(f"Saved OpenCV exercise outputs -> {OUT_DIR}")


if __name__ == "__main__":
    main()
