# common/utilities

Setup help and small standalone tools that don't belong to any one
week.

| File | What it's for |
|---|---|
| `environment_setup.md` | One combined guide to setting up Python + PyTorch (+ optionally CUDA) for the whole course. |
| `requirements-common.txt` | The union of every week's `requirements.txt` — handy if you'd rather set up one environment for the whole course instead of one per week. |
| `check_setup.py` | Run this any time to sanity-check your environment: Python version, NumPy, OpenCV, PyTorch, and CUDA availability. |
| `git_cheatsheet.md` | Short reference for the Git/GitHub commands used in Week 1 and throughout the course. |

## Quick check

```bash
python3 common/utilities/check_setup.py
```
