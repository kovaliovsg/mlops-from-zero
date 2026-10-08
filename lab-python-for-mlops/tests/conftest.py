"""Fixtures every test file can ask for by name."""
import pandas as pd
import pytest

from prep_forecast.generate import generate


@pytest.fixture(scope="session")
def order_books(tmp_path_factory):
    """Two months of order books, generated once for the whole test run (seed 7). Returns (folder, faults)."""
    folder = tmp_path_factory.mktemp("data")
    faults = generate(folder, seed=7, start="2024-01-01", end="2024-02-29")
    return folder, faults


@pytest.fixture
def menu():
    return pd.Series(["Margherita Pizza", "Caesar Salad", "Tomato Soup"])


@pytest.fixture
def few_orders():
    """Five hand-made rows, one problem each - small enough to check by eye."""
    return pd.DataFrame({
        "date": ["2024-03-01", "2024-03-01", "2024-02-30", "2024-03-02", "2024-03-02"],
        "branch": ["Harbor", "Harbor", "Harbor", None, "Harbor"],
        "service": ["lunch", "lunch", "dinner", "lunch", "dinner"],
        "dish": ["Margherita Pizza", "Margherita Pizza", "Caesar Salad", "Tomato Soup", " caesar salad "],
        "qty": [12.0, 12.0, 4.0, 3.0, 900.0],
        "promo": [False, False, False, False, False],
    })
