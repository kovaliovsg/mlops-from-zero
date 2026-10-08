"""Taste test: one dish, one branch. Same code, same data - is the score the same every run?"""
import argparse
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Two years of order books. The data is fixed (seed 7), so only the training can change.
rng = np.random.default_rng(7)
day = np.arange(730)
weekday, temp = day % 7, 15 + 10 * np.sin(day / 58) + rng.normal(0, 3, 730)
holiday, promo = rng.random(730) < 0.03, rng.random(730) < 0.1
sold = (40 + 12 * (weekday >= 4) + 0.6 * temp + 15 * holiday + 9 * promo + rng.normal(0, 2.5, 730)).round()
features = np.column_stack([weekday, temp, holiday, promo])

train, test = day < 640, day >= 640                 # learn from the past, test on the last 90 days
chef = sold[np.flatnonzero(test) - 7]               # the baseline: same day last week

parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int, default=None)
seed = parser.parse_args().seed

model = RandomForestRegressor(n_estimators=20, random_state=seed)
model.fit(features[train], sold[train])
guess = model.predict(features[test])

print(f"Chef's guess:  off by {mean_absolute_error(sold[test], chef):.2f} portions a day")
print(f"Model:         off by {mean_absolute_error(sold[test], guess):.2f} portions a day   (seed: {seed})")
