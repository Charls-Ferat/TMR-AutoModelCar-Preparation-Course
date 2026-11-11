# Week 2 — Introduction to Machine Learning

## Learning goals
- Understand supervised learning: image in, number out.
- Build a small CNN in PyTorch.
- Split data into training/validation sets, train, and read a loss curve.
- See overfitting happen on purpose, and know how to recognize it.

## The task
We reuse Week 1's idea of a ball moving across a frame. This week the
question is: **given only the image, can a CNN predict the ball's
horizontal position (a number between 0 and 1)?**

This is deliberately simple — one clear number to predict — so we can
focus entirely on the *machine learning workflow*. Week 3 swaps this toy
task for real steering prediction using the exact same code.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

This week adds PyTorch and matplotlib on top of Week 1's dependencies.

## Scripts (run in order)

| Script | What it does |
|---|---|
| `src/01_make_dataset.py` | Generates `data/ball_dataset/` — images of a moving ball plus `labels.csv` (filename, target position). Reuses `common.python.synthetic_data`. |
| `src/02_explore_dataset.py` | Loads the dataset with `common.python.dataset.CSVImageDataset` and previews a few (image, label) pairs. |
| `src/03_train.py` | Trains `SmallCNN` (from `common.python.cnn`) to predict ball position. Saves the trained model and a loss-curve plot. |
| `src/04_overfit_demo.py` | Trains the *same* model on a tiny slice of data with no regularization, so you can clearly see train loss keep dropping while validation loss rises. |

Run them from this folder:

```bash
python3 src/01_make_dataset.py
python3 src/02_explore_dataset.py
python3 src/03_train.py
python3 src/04_overfit_demo.py
```

## What's reused from Week 1 / common/

- `common.python.synthetic_data.render_ball_frame` — same rendering
  function used to make Week 1's video, now used to make a labeled
  dataset directly.
- `common.python.dataset.CSVImageDataset` and `train_val_split` — the
  same dataset class Week 3 and Week 4 will use for steering data.
- `common.python.cnn.SmallCNN` — the same architecture Week 3 predicts
  steering angles with.
- `common.python.train_utils.fit` / `plot_history` — the same training
  loop Week 3 and Week 4 reuse.

## Key concepts to walk through in class
- **Loss function**: we use Mean Squared Error (`nn.MSELoss`) because the
  target is a continuous number, not a category.
- **Train/validation split**: `train_val_split` in `common/python/dataset.py`.
- **Overfitting**: run `04_overfit_demo.py` and look at
  `data/overfit_loss.png` — 12 training images get a fixed random
  label-noise offset added, so the model can only keep improving train
  loss by *memorizing* those exact noisy labels. Train loss falls all
  the way to ~0, while validation loss (clean labels) bottoms out early
  and then climbs back up. That widening gap, and the fact that the
  best validation score happened epochs before training "finished", is
  overfitting. Discuss why (too little data, too much capacity, too
  many epochs) and what fixes exist (more data, augmentation, early
  stopping, weight decay, dropout).

## Exercises
1. In `03_train.py`, change `image_size` and see how it affects training time.
2. In `04_overfit_demo.py`, try increasing the training set size and see
   the overfitting gap shrink.
3. Add `weight_decay=1e-4` to the optimizer in `04_overfit_demo.py` and
   compare the new loss curve to the original.
