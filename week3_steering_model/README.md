# Week 3 — Steering Model

## Learning goals
- Build an image → steering-angle regression pipeline: exactly Week 2's
  workflow, applied to a real driving-relevant target.
- Evaluate a trained model against real steering values (not just loss
  curves): predicted vs. actual plots, error statistics.
- Know how to swap in a real TMR driving log later.

## The task
Given a camera frame of the road ahead, predict the steering value the
car should apply (a single float, typically in `[-1, 1]`: negative =
left, positive = right — check your TMR car's actual convention before
deploying this on the real car).

This is the same "image in, number out" problem as Week 2's ball
position, so we reuse the dataset class, the CNN, and the training loop
completely unchanged. What's new this week is the dataset itself (a
synthetic road instead of a ball) and, importantly, **evaluation**:
looking at predicted vs. actual steering, not just the loss number.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Same dependencies as Week 2 (NumPy, OpenCV, PyTorch, Matplotlib).

## Scripts (run in order)

| Script | What it does |
|---|---|
| `src/01_make_dataset.py` | Generates `data/steering_dataset/`: road images + `labels.csv` (filename, steering). Uses `common.python.synthetic_data.generate_steering_dataset` directly — no new code needed. |
| `src/02_train.py` | Trains `SmallCNN` to predict steering from the image. Same `common.python.train_utils.fit` call as Week 2, just a different dataset and label column. |
| `src/03_evaluate.py` | Loads the trained model, runs it on the validation set, and produces: a predicted-vs-actual scatter plot, an error-over-samples plot, and printed error statistics (MAE, RMSE, max error). |
| `src/04_replace_with_real_data.md` | Short guide: how to point this exact pipeline at a real recorded TMR driving log instead of synthetic data. |

Run them from this folder:

```bash
python3 src/01_make_dataset.py
python3 src/02_train.py
python3 src/03_evaluate.py
```

## What's reused from Week 1/2 / common/

- `common.python.synthetic_data.generate_steering_dataset` — builds the
  labeled dataset directly (same idea as Week 2's `01_make_dataset.py`,
  just calling a common helper instead of writing the loop again).
- `common.python.dataset.CSVImageDataset` / `train_val_split` — identical
  to Week 2, just with `label_cols=["steering"]`.
- `common.python.cnn.SmallCNN` — the exact same architecture as Week 2.
- `common.python.train_utils.fit` / `plot_history` — the exact same
  training loop as Week 2.

The only genuinely new code this week is the **evaluation script**,
because "how good is my steering model, really?" needs more than a
final loss number.

## Key concepts to walk through in class
- Why steering prediction is regression, not classification.
- Reading a predicted-vs-actual scatter plot: points on the diagonal =
  perfect predictions; systematic bias shows up as an off-diagonal shift.
- Why Mean Absolute Error (MAE) is often more interpretable for steering
  than Mean Squared Error (a 0.2 average steering error is meaningful;
  a 0.04 average *squared* error is not).
- Where this breaks down on a real car: label noise from a human driver,
  distribution shift between recorded track and race track, latency
  (previewed further in Week 4).

## Exercises
1. In `01_make_dataset.py`, increase `num_samples` and re-train — how
   much does MAE improve?
2. In `03_evaluate.py`, find the 5 worst predictions and open those
   images — do they share something in common (e.g. sharp curves)?
3. Read `04_replace_with_real_data.md` and describe, in your own words,
   the 3 things you'd need to change to run this on real TMR data.
