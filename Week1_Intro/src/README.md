# Week 1 — Git + Python for Vision

## Learning goals
- Use Git/GitHub for version control (branches, commits, pull requests).
- Get comfortable with Python, NumPy arrays, and OpenCV images.
- Record (or generate) a video, then extract and manipulate frames from it.

By the end of this week you can turn a video into a folder of individual
frames and do basic NumPy/OpenCV operations on them — the same operations
you'll use to preprocess camera images for the TMR car all course long.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

This week only needs OpenCV and NumPy — no PyTorch yet.

## Git warm-up

Before touching any code, do the Git exercise:
1. Create a GitHub repository for your course work.
2. Clone it locally, copy this `week1_git_python_vision/` folder into it.
3. Make a branch `week1`, commit your changes as you go, open a pull
   request into `main` when you're done.

A short command reference is in `../common/utilities/git_cheatsheet.md`.

## Scripts (run in order)

| Script | What it does |
|---|---|
| `src/01_generate_or_record_video.py` | Records 5s from your webcam if one is available, otherwise generates a synthetic video — either way you get `data/input_video.mp4`. |
| `src/02_extract_frames.py` | Extracts frames from that video into `data/frames/`. |
| `src/03_numpy_basics.py` | Loads a frame and manipulates it as a plain NumPy array: grayscale, crop, flip, brightness stats. |
| `src/04_opencv_playground.py` | OpenCV operations: color spaces, blurring, edge detection, drawing overlays — saved to `data/opencv_outputs/`. |

Run them from this folder:

```bash
python3 src/01_generate_or_record_video.py
python3 src/02_extract_frames.py
python3 src/03_numpy_basics.py
python3 src/04_opencv_playground.py
```

## Where the reused code lives

All four scripts import shared helpers from `../common/python/`
(`video_utils.py`, `image_utils.py`, `synthetic_data.py`) instead of
re-implementing video I/O — this is the same code Weeks 2–4 build on.

## Exercises
1. Change `every_n` in `02_extract_frames.py` and see how many frames you get.
2. In `03_numpy_basics.py`, compute the average brightness of the *left half*
   vs the *right half* of a frame using pure NumPy slicing.
3. In `04_opencv_playground.py`, try a different edge-detection threshold
   and describe what changes.
4. Commit each exercise as a separate Git commit with a clear message.
