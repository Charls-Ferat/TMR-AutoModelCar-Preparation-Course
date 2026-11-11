"""
live_steering_demo.py
------------------------
OPTIONAL "close the loop" demo: run the exact steering CNN trained in
week3_steering_model (or week4_gpu_cuda) on live webcam frames and stream
the predictions to the MBot over serial, using mbot_serial.py.

This script intentionally reuses, unchanged:
  - common.python.cnn.SmallCNN            (the model architecture)
  - common.python.image_utils.to_tensor   (image -> model input)
  - this folder's mbot_serial.py           (model output -> UART packet)

Run from the repository root so the `common` package can be found:
    python3 week5_robotics_mbot/host_side/live_steering_demo.py \
        --model week3_steering_model/data/steering_cnn.pt \
        --port /dev/ttyUSB0

Needs: torch, opencv-python, pyserial (the course's usual dependencies
plus pyserial from this folder's requirements.txt).
"""
import argparse
import sys
import time
from pathlib import Path

import cv2
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root
from common.python.cnn import SmallCNN
from common.python.image_utils import to_tensor
from mbot_serial import build_packet

IMAGE_SIZE = (64, 64)  # must match the size the model was trained with


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Path to a trained steering_cnn.pt")
    parser.add_argument("--port", required=True, help="Serial port the MBot is on")
    parser.add_argument("--camera", type=int, default=0, help="Webcam index")
    parser.add_argument("--speed", type=int, default=120, help="Constant forward speed (0-255)")
    parser.add_argument("--rate-hz", type=float, default=20.0)
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = SmallCNN(in_channels=3, out_features=1, image_size=IMAGE_SIZE[0])
    model.load_state_dict(torch.load(args.model, map_location=device))
    model.to(device)
    model.eval()
    print(f"Loaded model from {args.model}, running on {device}")

    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {args.camera}")

    import serial
    with serial.Serial(args.port, 115200, timeout=0) as ser:
        print(f"Connected to {args.port}. Driving at speed={args.speed}. Ctrl+C to stop.")
        period_s = 1.0 / args.rate_hz
        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    continue

                tensor = to_tensor(frame, size=IMAGE_SIZE).unsqueeze(0).to(device)
                with torch.no_grad():
                    steering = model(tensor).item()

                steer_byte = int(round(max(-1.0, min(1.0, steering)) * 40))
                ser.write(build_packet(speed=args.speed, steer=steer_byte))

                time.sleep(period_s)
        except KeyboardInterrupt:
            print("\nStopping -- sending final 'stop' packet.")
            ser.write(build_packet(speed=0, steer=0))
        finally:
            cap.release()


if __name__ == "__main__":
    main()
