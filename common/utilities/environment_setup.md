# Environment setup

## 1. Python

Python 3.9–3.12 works for every week of this course. Check your version:

```bash
python3 --version
```

## 2. Virtual environment (recommended)

Create one environment for the whole course:

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r common/utilities/requirements-common.txt
```

Or create a fresh environment per week using that week's own
`requirements.txt` if you prefer to keep them isolated.

## 3. PyTorch: CPU vs GPU

`pip install torch` gives you a working CPU build on any machine — this
is all you need for Weeks 1–3 and for following along in Week 4.

If your machine (or the TMR car's onboard computer) has an NVIDIA GPU
and you want the GPU comparison in Week 4 to actually use it, install a
CUDA-enabled PyTorch build matching your installed CUDA driver version
instead. Find the exact command for your system at:
https://pytorch.org/get-started/locally/

Check what you actually got:

```bash
python3 -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

or just run `common/utilities/check_setup.py` (below).

## 4. Verify everything at once

```bash
python3 common/utilities/check_setup.py
```

This prints your Python version and whether NumPy, OpenCV, PyTorch, and
CUDA are available — run it before Week 1 and again before Week 4.

## 5. Git/GitHub

Needed from Week 1 onward. See `git_cheatsheet.md` in this folder if
you're new to Git.
