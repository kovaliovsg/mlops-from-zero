"""prepare - the laminated recipe card: raw order books in, one clean row per dish, branch and day out.

    prepare                                   # settings from config.toml
    prepare --input data --max-qty 400        # a command line value beats the file
    python -m prep_forecast.prepare --help    # the same, without the installed command

Exit status, so a pipeline knows how it went: 0 done, 1 the data or a file was wrong (the log says what),
2 the command line was wrong (argparse says what).
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
import tomllib
from pathlib import Path

from prep_forecast.cleaning import clean_orders, daily_demand, load_tables

logger = logging.getLogger(__name__)


def read_config(path: Path) -> dict:
    """The [prepare] table of a TOML file. tomllib only reads, and only from a file opened in binary mode."""
    if not path.exists():
        return {}
    with path.open("rb") as f:
        return tomllib.load(f).get("prepare", {})


def parse_args(argv: list[str] | None, config: dict) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="prepare", description="Clean the order books into daily demand.")
    parser.add_argument("--config", type=Path, default=Path("config.toml"),
                        help="TOML file with a [prepare] table (default: config.toml)")
    parser.add_argument("--input", type=Path, default=Path(config.get("input", "data")),
                        help="folder holding orders.csv, dishes.csv, branches.csv, weather.csv")
    parser.add_argument("--output", type=Path, default=Path(config.get("output", "data/daily_demand.parquet")),
                        help="Parquet file to write")
    parser.add_argument("--max-qty", type=int, default=config.get("max_qty", 500),
                        help="portions per service above which a row is a typo")
    parser.add_argument("--country", default=config.get("country", "US"), help="public holidays of this country")
    parser.add_argument("--log-level", default=os.environ.get("PREP_LOG_LEVEL", "INFO"),
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                        help="how much to log (default: INFO, or the PREP_LOG_LEVEL environment variable)")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    # Read --config first, so the file can supply the other defaults.
    early = argparse.ArgumentParser(add_help=False)
    early.add_argument("--config", type=Path, default=Path("config.toml"))
    config_path = early.parse_known_args(argv)[0].config
    args = parse_args(argv, read_config(config_path))

    # Configure logging once, here in the entry point; every module only asks for its own logger.
    logging.basicConfig(level=args.log_level, format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
                        datefmt="%H:%M:%S", force=True)

    try:
        tables = load_tables(args.input)
    except FileNotFoundError as err:
        logger.error("cannot read the order books: %s", err)
        logger.error("make them first: python -m prep_forecast.generate")
        return 1

    orders, report = clean_orders(tables["orders"], tables["dishes"]["dish"], args.max_qty)
    if report["rows_out"] < 0.9 * report["rows_in"]:
        logger.error("more than 10%% of the rows were dropped - check the data before trusting it")
        return 1

    daily = daily_demand(orders, tables, args.country)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    daily.to_parquet(args.output, index=False)
    logger.info("wrote %d rows (%d branches x %d dishes x %d days) to %s", len(daily),
                daily["branch"].nunique(), daily["dish"].nunique(), daily["date"].nunique(), args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
