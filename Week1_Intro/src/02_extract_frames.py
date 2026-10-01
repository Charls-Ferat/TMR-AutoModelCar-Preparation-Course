import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from common.python.video_utils import extract_frames, get_video_info

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INPUT_VIDEO = DATA_DIR / "input_video.mp4"
FRAMES_DIR = DATA_DIR / "frames"


def main():
    if not INPUT_VIDEO.exists():
        raise FileNotFoundError(
            f"{INPUT_VIDEO} not found. Run 01_generate_or_record_video.py first."
        )

    info = get_video_info(str(INPUT_VIDEO))
    print(f"Video info: {info}")

    # every_n=2 keeps every second frame
    paths = extract_frames(str(INPUT_VIDEO), str(FRAMES_DIR), every_n=2)
    print(f"Extracted {len(paths)} frames -> {FRAMES_DIR}")


if __name__ == "__main__":
    main()
