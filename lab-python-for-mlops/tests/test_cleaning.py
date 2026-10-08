"""The cleaning rules, one at a time, on rows small enough to check by eye."""
import pandas as pd
import pytest

from prep_forecast.cleaning import clean_orders, daily_demand, load_tables, tidy_dish_names


@pytest.mark.parametrize("raw, expected", [
    ("Margherita Pizza", "Margherita Pizza"),
    (" margherita pizza ", "Margherita Pizza"),
    ("CAESAR SALAD", "Caesar Salad"),
    ("Chocolate Cake", None),          # not on the menu
])
def test_tidy_dish_names(raw, expected, menu):
    result = tidy_dish_names(pd.Series([raw]), menu).iloc[0]
    assert result == expected if expected else pd.isna(result)


def test_every_problem_row_is_counted(few_orders, menu):
    clean, report = clean_orders(few_orders, menu, max_qty=500)
    assert report["duplicate_row"] == 1
    assert report["bad_date"] == 1            # 30 February
    assert report["missing_branch"] == 1
    assert report["huge_qty"] == 1            # 900 portions of salad at one dinner
    assert report["dish_name_fixed"] == 1
    assert len(clean) == report["rows_out"] == 1


def test_clean_rows_are_clean(few_orders, menu):
    clean, _ = clean_orders(few_orders, menu, max_qty=500)
    assert clean["date"].dtype.kind == "M"    # real dates, not text
    assert clean["qty"].dtype == "int64"
    assert clean.notna().all().all()


def test_the_planted_mistakes_are_all_found(order_books):
    folder, planted = order_books
    tables = load_tables(folder)
    _, report = clean_orders(tables["orders"], tables["dishes"]["dish"], max_qty=500)
    for fault, count in planted.items():
        if fault != "messy_dish_name":
            assert report[fault] == count, fault
    assert report["dish_name_fixed"] == planted["messy_dish_name"]
    assert report["unknown_dish"] == 0


def test_one_row_per_day_branch_and_dish(order_books):
    folder, _ = order_books
    tables = load_tables(folder)
    clean, _ = clean_orders(tables["orders"], tables["dishes"]["dish"], max_qty=500)
    daily = daily_demand(clean, tables)
    assert not daily.duplicated(["date", "branch", "dish"]).any()
    assert len(daily) == 60 * 5 * 12                  # 60 days x 5 branches x 12 dishes, gaps included
    assert daily["qty"].sum() == clean["qty"].sum()   # nothing lost or double-counted on the way


def test_a_day_with_no_clean_orders_stays_as_a_gap(order_books):
    folder, _ = order_books
    tables = load_tables(folder)
    clean, _ = clean_orders(tables["orders"], tables["dishes"]["dish"], max_qty=500)
    gone = (clean["date"] == "2024-01-10") & (clean["branch"] == "Harbor") & (clean["dish"] == "Lasagna")
    daily = daily_demand(clean.loc[~gone], tables)
    row = daily[(daily["date"] == "2024-01-10") & (daily["branch"] == "Harbor") & (daily["dish"] == "Lasagna")]
    assert len(row) == 1 and pd.isna(row["qty"].iloc[0])


def test_a_menu_with_a_dish_twice_is_refused(order_books):
    folder, _ = order_books
    tables = load_tables(folder)
    clean, _ = clean_orders(tables["orders"], tables["dishes"]["dish"], max_qty=500)
    tables["dishes"] = pd.concat([tables["dishes"], tables["dishes"].head(1)])
    with pytest.raises(pd.errors.MergeError, match="not a many-to-one merge"):
        daily_demand(clean, tables)


def test_holidays_are_marked(order_books):
    folder, _ = order_books
    tables = load_tables(folder)
    clean, _ = clean_orders(tables["orders"], tables["dishes"]["dish"], max_qty=500)
    daily = daily_demand(clean, tables)
    new_year = daily.loc[daily["date"] == "2024-01-01", "is_holiday"]
    assert new_year.all() and not daily.loc[daily["date"] == "2024-01-03", "is_holiday"].any()


def test_takings_add_up_both_ways(order_books):
    folder, _ = order_books
    tables = load_tables(folder)
    clean, _ = clean_orders(tables["orders"], tables["dishes"]["dish"], max_qty=500)
    daily = daily_demand(clean, tables)
    takings = daily["qty"] * daily["price"]
    # Money is a float: summed in a different order it can differ in the last digit, so compare with approx.
    assert takings.groupby(daily["branch"]).sum().sum() == pytest.approx(takings.sum())
