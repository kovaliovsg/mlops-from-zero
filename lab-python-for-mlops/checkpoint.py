"""The taste test for this lab: is the prep-forecast repo standing up properly?

Checks, in order: you are inside the lab's own .venv, the order books exist, prepare made one clean row per
day, branch and dish, and every test passes. Prints CHECKPOINT OK only when all of that is true.
"""
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
DAILY = HERE / "data" / "daily_demand.parquet"
problems = []

if sys.prefix == sys.base_prefix:
    problems.append("not running inside a virtual environment - activate .venv first (step 1)")
if not (HERE / "data" / "orders.csv").exists():
    problems.append("no data/orders.csv - run: python -m prep_forecast.generate (step 3)")
if not DAILY.exists():
    problems.append("no data/daily_demand.parquet - run: prepare (step 6)")
else:
    daily = pd.read_parquet(DAILY)
    print(f"daily_demand.parquet: {len(daily):,} rows, {daily['qty'].sum():,} portions")
    if len(daily) != 5 * 12 * 1369:
        problems.append(f"expected 82,140 rows (5 branches x 12 dishes x 1,369 days), found {len(daily):,}")
    if daily.duplicated(["date", "branch", "dish"]).any():
        problems.append("some day, branch and dish appears twice")
    if (daily["qty"] < 0).any() or (daily["qty"] > 1000).any():
        problems.append("impossible portion counts are still in the table")

tests = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"],
                       cwd=HERE, capture_output=True, text=True)
summary = (tests.stdout.strip().splitlines() or ["(no output)"])[-1]
print(f"pytest: {summary}")
if tests.returncode != 0:
    problems.append(f"pytest exited with {tests.returncode} - run: pytest (step 7)")

for problem in problems:
    print("  -", problem)
print("CHECKPOINT OK" if not problems else "CHECKPOINT FAILED")
sys.exit(0 if not problems else 1)
