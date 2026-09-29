"""
These functions generate small, fake-but-useful
image datasets so every notebook/script in this course runs end-to-end
out of the box. As soon as you have real TMR camera + steering-log data,
swap it in

Two generators:
  * render_ball_frame(t)      -> a frame with a ball moving left/right.
                                  Used in Week 1 (video) and Week 2
                                  (image -> number regression).
  * render_road_frame(steer)  -> a frame that looks like a simple road
                                  with a bend. Used in Week 3 (image ->
                                  steering angle), in the same format as
                                  a real TMR driving log.
"""

import math

import cv2
import numpy as np


def render_ball_frame(t: float, size=(160, 120)):
    """
    Draw one frame with a bright ball moving sinusoidally left-right.

    t : float in [0, 1] -- position along the sequence in time.
    Returns (frame_bgr, x_norm) where x_norm in [0, 1] is the ball's
    horizontal position -- this is the "numerical output" a Week 2
    student's CNN will learn to predict from the image.
    """
    w, h = size
    frame = np.full((h, w, 3), 30, dtype=np.uint8)  # dark gray background

    x_norm = 0.5 + 0.45 * math.sin(2 * math.pi * t)   # in [0.05, 0.95]
    cx = int(x_norm * w)
    cy = h // 2

    cv2.circle(frame, (cx, cy), radius=max(4, h // 10), color=(60, 180, 255), thickness=-1)
    return frame, x_norm


def render_road_frame(steering: float, size=(160, 120)):
    """
    Draw one frame that looks like a simple road seen from the TMR car's
    front camera, curving according to `steering`.

    steering : float in [-1, 1] -- negative = curve/steer left,
               positive = curve/steer right (matches typical TMR
               steering-command convention).
    Returns frame_bgr only -- the label is `steering` itself, which you
    already know when generating the dataset.
    """
    w, h = size
    frame = np.full((h, w, 3), (40, 40, 40), dtype=np.uint8)  # asphalt gray

    # Lane center follows a curve whose sharpness/direction is `steering`.
    # y=0 at the top (far away) ... y=h at the bottom (close to the car).
    lane_pts_left, lane_pts_right = [], []
    lane_half_width = w * 0.28
    for y in range(0, h, 2):
        depth = 1.0 - (y / h)                      # 1 = far away, 0 = close
        curve_offset = steering * (w * 0.35) * (depth ** 2)
        center_x = w / 2 + curve_offset
        lane_pts_left.append((int(center_x - lane_half_width * (0.3 + 0.7 * depth)), y))
        lane_pts_right.append((int(center_x + lane_half_width * (0.3 + 0.7 * depth)), y))

    cv2.polylines(frame, [np.array(lane_pts_left, dtype=np.int32)], False, (230, 230, 230), 3)
    cv2.polylines(frame, [np.array(lane_pts_right, dtype=np.int32)], False, (230, 230, 230), 3)
    return frame


def generate_ball_sequence(num_frames=200, size=(160, 120)):
    """Yield (frame, x_norm) pairs for a full ball sequence, t in [0, 1]."""
    for i in range(num_frames):
        t = i / num_frames
        yield render_ball_frame(t, size=size)


def generate_steering_dataset(out_dir, num_samples=600, size=(160, 120), seed=0):
    """
    Build a small labeled image dataset that mimics a real TMR driving
    log: a folder of JPEGs plus a `labels.csv` with columns
    `filename,steering`. Returns the path to labels.csv.
    """
    import csv
    import os
    from pathlib import Path

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    csv_path = os.path.join(out_dir, "labels.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "steering"])
        for i in range(num_samples):
            steering = float(np.clip(rng.normal(0.0, 0.5), -1.0, 1.0))
            frame = render_road_frame(steering, size=size)
            # small amount of pixel noise: real cameras are never perfectly clean
            noise = rng.normal(0, 6, frame.shape).astype(np.int16)
            frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            filename = f"road_{i:05d}.jpg"
            cv2.imwrite(os.path.join(out_dir, filename), frame)
            writer.writerow([filename, f"{steering:.4f}"])

    return csv_path
