"""Spot the drift - the lab for "What is MLOps?".

A restaurant's model forecasts how many portions of cold soup it will sell from the temperature outside.
It is trained on spring days, then it meets two kinds of change:
  data drift    - a heatwave: temperatures it has never seen
  concept drift - a competitor opens next door: same temperatures, fewer customers
"""
import numpy as np
from sklearn.linear_model import LinearRegression

rng = np.random.default_rng(7)


def portions_sold(temp, competitor=False):
    """The real world. Sales rise with heat up to about 30 C; in a heatwave people stay indoors."""
    sold = np.where(temp <= 30, 4 * temp, 120 - 6 * (temp - 30))
    if competitor:
        sold = sold * 0.6
    return np.clip(sold + rng.normal(0, 4, len(temp)), 0, None)


def average_error(model, temp, sold):
    return np.abs(model.predict(temp.reshape(-1, 1)) - sold).mean()


spring = rng.uniform(10, 28, 200)
model = LinearRegression().fit(spring.reshape(-1, 1), portions_sold(spring))
print(f"Trained on 200 spring days ({spring.min():.0f}-{spring.max():.0f} C), average {spring.mean():.1f} C.")

more_spring = rng.uniform(10, 28, 60)
e1 = average_error(model, more_spring, portions_sold(more_spring))
print(f"Check 1, more spring days:   average {more_spring.mean():.1f} C  -> average error {e1:5.1f} portions")

heatwave = rng.uniform(32, 40, 60)
e2 = average_error(model, heatwave, portions_sold(heatwave))
print(f"Check 2, a heatwave:         average {heatwave.mean():.1f} C  -> average error {e2:5.1f} portions  <- data drift: the inputs moved")

competitor = rng.uniform(10, 28, 60)
e3 = average_error(model, competitor, portions_sold(competitor, competitor=True))
print(f"Check 3, competitor opens:   average {competitor.mean():.1f} C  -> average error {e3:5.1f} portions  <- concept drift: inputs look normal")

print()
print("Notice: check 3's temperatures look exactly like spring. Watching the inputs alone would miss it;")
print("only comparing the forecast with the real sales shows the model went off.")
ok = e2 > 3 * e1 and e3 > 3 * e1
print("CHECKPOINT OK" if ok else "CHECKPOINT FAILED")
