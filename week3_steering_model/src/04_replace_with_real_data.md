# Using real TMR driving data instead of the synthetic dataset

Everything in this folder — `CSVImageDataset`, `SmallCNN`, `fit`,
`03_evaluate.py` — works unchanged on real data, as long as your data
matches the same simple format:

```
your_dataset/
├── labels.csv       # columns: filename,steering
├── frame_00000.jpg
├── frame_00001.jpg
└── ...
```

## Steps to switch over

1. **Record a driving log on the TMR car.** Save camera frames (reuse
   Week 1's `extract_frames` on a recorded drive video) together with
   the steering command that was active at each frame's timestamp.
2. **Write a `labels.csv`** with a `filename` column matching your saved
   images and a `steering` column with the recorded steering value at
   that moment (match by timestamp — this is the fiddly part, budget
   real time for it).
3. **Point `DATASET_DIR` in `02_train.py` and `03_evaluate.py`** at your
   new folder instead of `data/steering_dataset`. Nothing else changes.
4. **Re-check `IMAGE_SIZE`** — real camera frames are usually larger
   than 64x64; a slightly bigger size (e.g. 96x96) is a reasonable start,
   but bigger images mean slower training (see Week 4 for GPU speed-ups).
5. **Re-run evaluation and actually look at the worst predictions'
   images** — synthetic data doesn't have lighting changes, motion blur,
   or an inattentive human driver mid-log. Real data does.

## Common pitfalls with real driving logs
- **Timestamp misalignment** between camera and steering log — double
  check frames and labels are actually synchronized.
- **Imbalanced steering distribution** — most driving is close to
  "straight", so a lazy model that always predicts ~0 steering can still
  get a deceptively low MAE. Look at the predicted-vs-actual plot, not
  just the average error, to catch this.
- **Overfitting to one track layout** (this is exactly Week 2's
  overfitting lesson, applied here) — validate on a drive recorded on a
  *different* part of the track if you can.
