"""
Get video in and out of OpenCV:
  * record from a webcam
  * write a list of frames to an .mp4 file
  * extract frames from a video file to disk
"""

import os
from pathlib import Path

import cv2
import numpy as np


def open_camera(source=0) -> cv2.VideoCapture:
    """Open a camera (or video file) and fail loudly with a clear message."""
    cap = cv2.VideoCapture(source, cv2.CAP_V4L2)
    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open camera/source '{source}'. "
            "If you are on a machine without a webcam, use the synthetic "
            "video generator instead (see synthetic_data.py)."
        )

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    
    return cap


def record_video_from_camera(output_path: str, seconds: float = 5.0,
                              source=0, fps: int = 20,
                              size: tuple = (320, 180)) -> str:
    """
    Record `seconds` of video from a camera and save it as an .mp4.
    Returns the output path. Raises RuntimeError if no camera is found --
    catch that and fall back to a synthetic video in the classroom.
    """
    cap = open_camera(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
    n_frames = int(seconds * fps)
    for _ in range(n_frames):
        ok, frame = cap.read()
        if not ok:
            break
        frame = cv2.resize(frame, size)
        writer.write(frame)

    cap.release()
    writer.release()
    return output_path

def write_frames_to_video(frames, output_path: str, fps: int = 20) -> str:
    """Write a list/iterable of BGR NumPy frames to an .mp4 file."""
    frames = list(frames)
    if not frames:
        raise ValueError("No frames to write.")
    h, w = frames[0].shape[:2]
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    for frame in frames:
        writer.write(frame)
    writer.release()
    return output_path


def get_video_info(video_path: str) -> dict:
    """Return basic metadata about a video file."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    info = {
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    cap.release()
    return info


def extract_frames(video_path: str, out_dir: str, every_n: int = 1,
                    prefix: str = "frame") -> list:
    """
    Extract frames from `video_path` into `out_dir` as JPEGs.
    Keeps every `every_n`-th frame (1 = keep all frames).
    Returns the list of saved file paths.
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")

    saved_paths = []
    frame_idx = 0
    saved_idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if frame_idx % every_n == 0:
            out_path = os.path.join(out_dir, f"{prefix}_{saved_idx:05d}.jpg")
            cv2.imwrite(out_path, frame)
            saved_paths.append(out_path)
            saved_idx += 1
        frame_idx += 1

    cap.release()
    return saved_paths


def frame_generator_from_video(video_path: str):
    """Yield frames from a video one at a time (memory-friendly)."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {video_path}")
    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            yield frame
    finally:
        cap.release()
