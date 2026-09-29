# common/python

Small, dependency-light modules reused across all four weeks. Import them
directly in your own projects:

```python
from common.python.cnn import SmallCNN
from common.python.dataset import CSVImageDataset, train_val_split
from common.python.train_utils import fit, plot_history
```

| Module              | What it gives you                                                        | First used |
|---------------------|---------------------------------------------------------------------------|------------|
| `video_utils.py`     | Open a camera, record video, extract frames from a video, write frames to a video | Week 1 |
| `synthetic_data.py`  | Generate small fake-but-useful datasets (moving ball, curving road) so every exercise runs without real hardware | Week 1–3 |
| `image_utils.py`     | Load images, convert BGR↔RGB, resize, turn an image into a normalized PyTorch tensor | Week 1–4 |
| `dataset.py`         | `CSVImageDataset`: a generic `(image, label)` dataset from a folder of images + a `labels.csv` | Week 2–4 |
| `cnn.py`             | `SmallCNN`: one small, readable CNN reused unchanged across weeks | Week 2–4 |
| `train_utils.py`     | Generic train/validate loop + loss-curve plotting | Week 2–4 |

**Why "reusable"?** Every week's `src/` scripts import from here instead of
re-implementing the same 20 lines. When you start your own TMR project,
copy this whole `common/` folder into it and keep going.

No ROS2 or CUDA-specific code lives here — see `../ros2` and each week's
own `src/` for that.
