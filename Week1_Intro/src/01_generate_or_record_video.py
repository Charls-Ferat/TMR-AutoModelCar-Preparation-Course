import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # repo root
from common.python.video_utils import record_video_from_camera, write_frames_to_video
from common.python.synthetic_data import generate_ball_sequence

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUTPUT_VIDEO = DATA_DIR / "input_video.mp4"


def main():
    DATA_DIR.mkdir(exist_ok=True)

    try:
        print("Trying to record 5 seconds from your webcam...")
        record_video_from_camera(str(OUTPUT_VIDEO), seconds=5, source=0)
        print(f"Recorded real webcam video -> {OUTPUT_VIDEO}")
    except RuntimeError as e:
        print(f"No webcam found ({e}).")
        print("Falling back to a synthetic video (a ball moving left/right).")
        frames = [frame for frame, _ in generate_ball_sequence(num_frames=100, size=(320, 180))]
        write_frames_to_video(frames, str(OUTPUT_VIDEO), fps=20)
        print(f"Generated synthetic video -> {OUTPUT_VIDEO}")


if __name__ == "__main__":
    main()
