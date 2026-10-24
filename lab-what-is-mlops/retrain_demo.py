"""Spot the drift, part 2 - the fix: retrain on fresh data.

The same restaurant, the same soup model and the same two changes as drift_demo.py (the same random seed, so the
"before" numbers match it). Then the kitchen does what monitoring asks for: it retrains the same code on the latest
days, and checks again on days the new model has not seen.
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


def train(temp, sold):
    return LinearRegression().fit(temp.reshape(-1, 1), sold)


def average_error(model, temp, sold):
    return np.abs(model.predict(temp.reshape(-1, 1)) - sold).mean()


# The same days as drift_demo.py, drawn in the same order.
spring = rng.uniform(10, 28, 200)
model = train(spring, portions_sold(spring))
more_spring = rng.uniform(10, 28, 60)
e1 = average_error(model, more_spring, portions_sold(more_spring))
heatwave = rng.uniform(32, 40, 60)
heatwave_sold = portions_sold(heatwave)
competitor = rng.uniform(10, 28, 60)
competitor_sold = portions_sold(competitor, competitor=True)

print("The spring model, before retraining:")
print(f"  heatwave days:     average error {average_error(model, heatwave, heatwave_sold):5.1f} portions")
print(f"  competitor days:   average error {average_error(model, competitor, competitor_sold):5.1f} portions")

# Retrain: the same code, on the 30 latest days of each new world. Check on 30 later days it has not seen.
recent_heat = rng.uniform(32, 40, 30)
heat_model = train(recent_heat, portions_sold(recent_heat))
later_heat = rng.uniform(32, 40, 30)
e2 = average_error(heat_model, later_heat, portions_sold(later_heat))

recent_comp = rng.uniform(10, 28, 30)
comp_model = train(recent_comp, portions_sold(recent_comp, competitor=True))
later_comp = rng.uniform(10, 28, 30)
e3 = average_error(comp_model, later_comp, portions_sold(later_comp, competitor=True))

print()
print("Retrained on the 30 latest heatwave days:")
print(f"  later heatwave days:    average error {e2:5.1f} portions")
print("Retrained on the 30 latest days with the competitor open:")
print(f"  later competitor days:  average error {e3:5.1f} portions")
print()
print("Same code, fresh data: the error is back near the spring level of "
      f"{e1:.1f} portions.")
ok = e2 < 2 * e1 and e3 < 2 * e1
print("CHECKPOINT OK" if ok else "CHECKPOINT FAILED")
