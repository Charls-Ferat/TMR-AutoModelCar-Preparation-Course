"""
Sanity-check the environment for this course:

    python3 common/utilities/check_setup.py

Safe to run at any point -- it only imports and reports, it doesn't
install or change anything.
"""
import sys


def check(name, import_fn):
    try:
        result = import_fn()
        print(f"[OK]   {name}: {result}")
        return True
    except ImportError as e:
        print(f"[MISS] {name}: not installed ({e})")
        return False


def main():
    print(f"Python: {sys.version.split()[0]}")

    check("numpy", lambda: __import__("numpy").__version__)
    check("opencv-python (cv2)", lambda: __import__("cv2").__version__)
    check("matplotlib", lambda: __import__("matplotlib").__version__)

    torch_ok = check("torch", lambda: __import__("torch").__version__)
    if torch_ok:
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"[INFO] CUDA available: {cuda_available}")
        if cuda_available:
            print(f"[INFO] GPU: {torch.cuda.get_device_name(0)}")
        else:
            print("[INFO] No GPU detected -- fine for Weeks 1-3 and for "
                  "following Week 4's CPU results.")


if __name__ == "__main__":
    main()
