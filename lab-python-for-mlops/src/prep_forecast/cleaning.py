"""From raw order books to one clean row per dish, branch and
day - the table every later lab trains on.

These are the notebook's cells, refactored into functions: each
one does one job, takes a table and gives a table back, so a test
can check it on five hand-made rows instead of 165,000 real ones.
"""
from __future__ import annotations

import logging
from pathlib import Path

import holidays
import pandas as pd

logger = logging.getLogger(__name__)

KEYS = ["date", "branch", "dish"]


def load_tables(folder: Path) -> dict[str, pd.DataFrame]:
    """Read the four CSV files. Dates stay text here on purpose:
    a bad date must not stop the whole read."""
    return {name: pd.read_csv(folder / f"{name}.csv")
            for name in ("orders", "dishes", "branches",
                         "weather")}


def tidy_dish_names(names: pd.Series,
                    menu: pd.Series) -> pd.Series:
    """' margherita pizza ' and 'MARGHERITA PIZZA' ->
    'Margherita Pizza'. A name not on the menu becomes NaN."""
    lookup = {name.casefold(): name for name in menu}
    return names.str.strip().str.casefold().map(lookup)


def clean_orders(
    orders: pd.DataFrame, menu: pd.Series, max_qty: int
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Fix what can be fixed, drop what cannot, and count every
    row that went. Returns (clean table, report)."""
    report: dict[str, int] = {"rows_in": len(orders)}
    df = orders.drop_duplicates()
    report["duplicate_row"] = report["rows_in"] - len(df)

    tidy = tidy_dish_names(df["dish"], menu)
    report["dish_name_fixed"] = int(
        (tidy.notna() & (tidy != df["dish"])).sum())
    df = df.assign(dish=tidy, date=pd.to_datetime(
        df["date"], format="%Y-%m-%d", errors="coerce"))
    checks = {
        "bad_date": df["date"].isna(),
        "missing_branch": df["branch"].isna(),
        "unknown_dish": df["dish"].isna(),
        "missing_qty": df["qty"].isna(),
        "negative_qty": df["qty"] < 0,
        "huge_qty": df["qty"] > max_qty,
    }
    bad = pd.Series(False, index=df.index)
    for name, mask in checks.items():
        # each bad row is counted once, under its first fault
        report[name] = int((mask & ~bad).sum())
        bad |= mask
    df = df.loc[~bad].astype({"qty": "int64"})
    report["rows_out"] = len(df)
    for name, n in report.items():
        logger.info("%-15s %7d", name, n)
    return df.reset_index(drop=True), report


def daily_demand(orders: pd.DataFrame,
                 tables: dict[str, pd.DataFrame],
                 country: str = "US") -> pd.DataFrame:
    """Lunch + dinner -> one row per day, branch and dish, with
    what a forecast needs to know about that day."""
    daily = (orders.groupby(KEYS, as_index=False)
             .agg(qty=("qty", "sum"), promo=("promo", "any")))

    # Every day, branch and dish gets a row - even one whose lunch
    # and dinner rows were both dropped. Its qty stays empty
    # (<NA>), so a forecast sees a gap instead of a day that
    # silently vanished.
    every_row = pd.MultiIndex.from_product(
        [pd.date_range(orders["date"].min(),
                       orders["date"].max(), freq="D"),
         sorted(tables["branches"]["branch"]),
         sorted(tables["dishes"]["dish"])], names=KEYS)
    daily = daily.set_index(KEYS).reindex(every_row).reset_index()
    daily = (daily.astype({"qty": "Int64", "promo": "boolean"})
             .fillna({"promo": False}))
    gaps = int(daily["qty"].isna().sum())
    if gaps:
        logger.warning("%d day-branch-dish rows have no clean"
                       " orders left - their qty is empty", gaps)

    weather = tables["weather"].assign(date=pd.to_datetime(
        tables["weather"]["date"], format="%Y-%m-%d"))
    daily = (
        daily
        .merge(tables["dishes"][["dish", "category", "price"]],
               on="dish", how="left", validate="many_to_one")
        .merge(tables["branches"], on="branch", how="left",
               validate="many_to_one")
        .merge(weather, on=["date", "branch"], how="left",
               validate="many_to_one"))

    years = range(daily["date"].dt.year.min(),
                  daily["date"].dt.year.max() + 1)
    days_off = holidays.country_holidays(country, years=years)
    daily["is_holiday"] = daily["date"].dt.date.map(
        lambda d: d in days_off)
    daily["weekday"] = daily["date"].dt.day_name()
    return daily.sort_values(KEYS, ignore_index=True)


def monthly_totals(daily: pd.DataFrame) -> pd.DataFrame:
    """Portions per branch per month - 'ME' is month end (pandas 3
    removed the old 'M')."""
    return (daily.set_index("date")
            .groupby("branch")["qty"]
            .resample("ME").sum()
            .unstack("branch"))
