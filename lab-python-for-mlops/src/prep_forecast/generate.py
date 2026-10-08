"""The order books of a five-branch restaurant chain, made up but realistic.

    python -m prep_forecast.generate            -> data/orders.csv, dishes.csv, branches.csv, weather.csv

Every number comes from a seeded random generator, so the same seed always writes the same files.
Demand moves with the weekday, the weather, public holidays, promotions and a slow upward trend.
Then a handful of mistakes are planted on purpose - the kind a real till and a tired manager make -
because finding them is the job. `--drift` changes tastes from 2026-01-01, for the monitoring lessons.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import holidays
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

START, END = "2023-01-01", "2026-09-30"

BRANCHES = pd.DataFrame(
    {
        "branch": ["Downtown", "Harbor", "Uptown", "Riverside", "Airport"],
        "city": ["Boston", "Boston", "Chicago", "Chicago", "Boston"],
        "size": [1.3, 1.0, 1.1, 0.8, 0.9],
    }
)

# dish, category, price, portions per service on an ordinary day, how much warm weather helps (+) or hurts (-)
DISHES = pd.DataFrame(
    [
        ("Margherita Pizza", "pizza", 14.0, 22, 0.0),
        ("Pepperoni Pizza", "pizza", 16.0, 18, 0.0),
        ("Caesar Salad", "salad", 11.0, 12, 0.9),
        ("Greek Salad", "salad", 12.0, 9, 1.0),
        ("Tomato Soup", "soup", 8.0, 10, -1.0),
        ("Minestrone", "soup", 9.0, 7, -1.0),
        ("Spaghetti Carbonara", "pasta", 17.0, 15, -0.2),
        ("Lasagna", "pasta", 18.0, 11, -0.4),
        ("Grilled Salmon", "main", 26.0, 8, 0.2),
        ("Ribeye Steak", "main", 34.0, 6, 0.0),
        ("Tiramisu", "dessert", 9.0, 10, 0.0),
        ("Gelato", "dessert", 7.0, 9, 1.2),
    ],
    columns=["dish", "category", "price", "base", "warm"],
)

SERVICES = {"lunch": 0.45, "dinner": 0.55}


def make_weather(days: pd.DatetimeIndex, rng: np.random.Generator) -> pd.DataFrame:
    """One row per branch per day: temperature (C) and rain (mm). Boston and Chicago share a climate."""
    parts = []
    doy = days.dayofyear.to_numpy()
    for branch in BRANCHES["branch"]:
        temp = 11 - 13 * np.cos(2 * np.pi * (doy - 15) / 365.25) + rng.normal(0, 3.5, len(days))
        rain = np.where(rng.random(len(days)) < 0.3, rng.gamma(1.5, 4.0, len(days)), 0.0)
        parts.append(pd.DataFrame({"date": days, "branch": branch,
                                   "temp_c": temp.round(1), "rain_mm": rain.round(1)}))
    return pd.concat(parts, ignore_index=True)


def make_orders(weather: pd.DataFrame, rng: np.random.Generator, drift: bool = False) -> pd.DataFrame:
    """One row per branch, day, service and dish: how many portions were sold."""
    days = pd.DatetimeIndex(weather["date"].unique())
    us_holidays = holidays.country_holidays("US", years=range(days.year.min(), days.year.max() + 1))
    is_holiday = np.array([d in us_holidays for d in days.date])
    holiday_by_day = pd.Series(is_holiday, index=days)

    grid = weather.merge(DISHES, how="cross")
    grid = pd.concat([grid.assign(service=s, share=v) for s, v in SERVICES.items()], ignore_index=True)
    grid = grid.merge(BRANCHES[["branch", "size"]], on="branch", validate="many_to_one")

    date = pd.DatetimeIndex(grid["date"])
    weekday_lift = np.select([date.dayofweek == 4, date.dayofweek == 5, date.dayofweek == 6,
                              date.dayofweek == 0], [1.25, 1.35, 1.10, 0.85], 1.0)
    warmth = (grid["temp_c"].to_numpy() - 12) / 10
    weather_lift = np.clip(1 + 0.18 * grid["warm"].to_numpy() * warmth, 0.4, 1.8)
    rain_lift = np.where(grid["rain_mm"].to_numpy() > 5, 0.85, 1.0)
    holiday_lift = np.where(holiday_by_day.reindex(date).to_numpy(), 1.3, 1.0)
    years = (date - pd.Timestamp(START)).days.to_numpy() / 365.25
    trend = 1 + 0.06 * years
    promo = rng.random(len(grid)) < 0.04
    promo_lift = np.where(promo, 1.3, 1.0)

    mean = (grid["base"].to_numpy() * grid["share"].to_numpy() * grid["size"].to_numpy()
            * weekday_lift * weather_lift * rain_lift * holiday_lift * trend * promo_lift)
    if drift:
        after = date >= pd.Timestamp("2026-01-01")
        tastes = np.where(grid["category"].to_numpy() == "salad", 1.6,
                          np.where(grid["category"].to_numpy() == "pizza", 0.75, 1.0))
        mean = np.where(after, mean * tastes, mean)

    orders = pd.DataFrame({
        "date": date.strftime("%Y-%m-%d"),
        "branch": grid["branch"],
        "service": grid["service"],
        "dish": grid["dish"],
        "qty": rng.poisson(mean).astype("float64"),
        "promo": promo,
    })
    return orders.sort_values(["date", "branch", "service", "dish"], ignore_index=True)


def plant_faults(orders: pd.DataFrame, rng: np.random.Generator) -> tuple[pd.DataFrame, dict[str, int]]:
    """The mistakes a real order book holds. Returns the damaged table and how many of each were planted."""
    df = orders.copy()
    shuffled = iter(rng.permutation(len(df)))

    def take(k: int) -> list[int]:
        """The next k rows of a shuffled list, so no row gets two mistakes."""
        return [next(shuffled) for _ in range(k)]

    faults = {"missing_qty": 80, "negative_qty": 15, "huge_qty": 6, "messy_dish_name": 200,
              "bad_date": 40, "missing_branch": 25}
    df.loc[take(faults["missing_qty"]), "qty"] = np.nan
    rows = take(faults["negative_qty"])
    df.loc[rows, "qty"] = -df.loc[rows, "qty"].clip(lower=1)
    rows = take(faults["huge_qty"])
    df.loc[rows, "qty"] = df.loc[rows, "qty"].clip(lower=6) * 100   # two extra zeros typed at the till
    rows = take(faults["messy_dish_name"])
    df.loc[rows, "dish"] = [f" {d.lower()} " if i % 2 else d.upper() for i, d in enumerate(df.loc[rows, "dish"])]
    rows = take(faults["bad_date"])
    df.loc[rows, "date"] = [d[:8] + "31" if d[5:7] in ("04", "06", "09", "11") else d[:5] + "02-30"
                            for d in df.loc[rows, "date"]]
    df.loc[take(faults["missing_branch"]), "branch"] = np.nan

    faults["duplicate_row"] = 120
    dupes = df.iloc[take(faults["duplicate_row"])]
    df = pd.concat([df, dupes]).sort_index(kind="stable").reset_index(drop=True)
    return df, faults


def generate(out_dir: Path, seed: int = 42, start: str = START, end: str = END,
             drift: bool = False) -> dict[str, int]:
    """Write the four CSV files into out_dir. Returns the planted faults, so a test can check they are found."""
    rng = np.random.default_rng(seed)
    days = pd.date_range(start, end, freq="D")
    weather = make_weather(days, rng)
    orders, faults = plant_faults(make_orders(weather, rng, drift), rng)

    out_dir.mkdir(parents=True, exist_ok=True)
    orders.to_csv(out_dir / "orders.csv", index=False)
    DISHES[["dish", "category", "price"]].to_csv(out_dir / "dishes.csv", index=False)
    BRANCHES[["branch", "city"]].to_csv(out_dir / "branches.csv", index=False)
    weather.assign(date=weather["date"].dt.strftime("%Y-%m-%d")).to_csv(out_dir / "weather.csv", index=False)
    logger.info("wrote %d order rows for %d days to %s", len(orders), len(days), out_dir)
    return faults


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the restaurant chain's order books as CSV files.")
    parser.add_argument("--out", type=Path, default=Path("data"), help="folder to write into (default: data)")
    parser.add_argument("--seed", type=int, default=42, help="same seed, same files (default: 42)")
    parser.add_argument("--drift", action="store_true", help="tastes change from 2026-01-01")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    faults = generate(args.out, seed=args.seed, drift=args.drift)
    logger.info("planted %d mistakes for you to find", sum(faults.values()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
