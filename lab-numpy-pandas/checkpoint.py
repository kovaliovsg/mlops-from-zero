"""Checkpoint: is data/orders.parquet the clean order book the notebook's clean-up writes?

    python checkpoint.py

Run it in the lab's terminal, inside (.venv), after the notebook's last cell. It prints CHECKPOINT OK, or what is wrong.
"""
import sys
from pathlib import Path

DATA = Path("data")


def fail(message: str) -> None:
    print(f"NOT YET: {message}")
    raise SystemExit(1)


# checked before pandas is imported: outside the .venv there is no pandas to import
if sys.prefix == sys.base_prefix:
    fail("this terminal is not inside the lab's .venv - run .venv\\Scripts\\Activate.ps1 first")
if sys.version_info[:2] != (3, 12):
    fail(f"this .venv runs Python {sys.version.split()[0]}; the lab needs 3.12")

import pandas as pd  # noqa: E402

if not (DATA / "orders.csv").exists():
    fail("data/orders.csv is missing - run: python generate.py")
if not (DATA / "orders.parquet").exists():
    fail("data/orders.parquet is missing - run the notebook to its last cell")

orders = pd.read_csv(DATA / "orders.csv")
clean = pd.read_parquet(DATA / "orders.parquet")
menu = pd.read_csv(DATA / "dishes.csv")["dish"]

if list(clean.columns) != ["date", "branch", "service", "dish", "qty", "promo"]:
    fail(f"unexpected columns {list(clean.columns)} - was it saved with index=False?")
if clean.duplicated().sum():
    fail(f"{clean.duplicated().sum()} copied rows left - drop_duplicates()")
if clean[["branch", "qty"]].isna().sum().sum():
    fail("rows with no branch or no qty left - dropna(subset=[...])")
if not ((clean["qty"] >= 0) & (clean["qty"] <= 500)).all():
    fail(f"qty runs from {clean['qty'].min():g} to {clean['qty'].max():g} - keep 0 to 500")
if not clean["dish"].isin(menu).all():
    fail(f"{(~clean['dish'].isin(menu)).sum()} dish names are not on the menu - .str.strip().str.title()")
if clean["qty"].dtype != "float64" or clean["promo"].dtype != "bool":
    fail(f"dtypes changed: qty {clean['qty'].dtype}, promo {clean['promo'].dtype}")
dropped = len(orders) - len(clean)
if dropped != 246:
    fail(f"{dropped} rows dropped; the 246 planted ones are 120 copies + 25 no branch + 80 no qty + 15 + 6 impossible")

print(f"orders.parquet: {len(clean):,} rows, {clean['branch'].nunique()} branches, {clean['dish'].nunique()} dishes")
print(f"dropped {dropped} rows; blanks 0, copies 0, qty from {clean['qty'].min():g} to {clean['qty'].max():g}")
print("CHECKPOINT OK")
