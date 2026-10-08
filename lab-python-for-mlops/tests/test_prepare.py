"""The prepare command, run the way a pipeline runs it: arguments in, a file and an exit status out."""
import pandas as pd
import pytest

from prep_forecast.prepare import main


def test_writes_the_daily_table(order_books, tmp_path):
    folder, _ = order_books
    out = tmp_path / "daily.parquet"
    assert main(["--input", str(folder), "--output", str(out), "--config", str(tmp_path / "none.toml")]) == 0
    daily = pd.read_parquet(out)
    assert {"date", "branch", "dish", "qty", "temp_c", "is_holiday"} <= set(daily.columns)


def test_missing_input_exits_with_1(tmp_path):
    assert main(["--input", str(tmp_path / "nowhere"), "--config", str(tmp_path / "none.toml")]) == 1


def test_a_wrong_argument_exits_with_2(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--max-qty", "lots"])
    assert exit_info.value.code == 2
    assert "invalid int value" in capsys.readouterr().err


def test_the_command_line_beats_the_config_file(order_books, tmp_path):
    folder, _ = order_books
    config = tmp_path / "config.toml"
    config.write_text(f'[prepare]\ninput = "{folder.as_posix()}"\nmax_qty = 1\n', encoding="utf-8")
    # max_qty = 1 in the file would drop almost every row (exit 1); the command line restores a sane cap
    assert main(["--config", str(config), "--output", str(tmp_path / "d.parquet"), "--max-qty", "500"]) == 0
    assert main(["--config", str(config), "--output", str(tmp_path / "d.parquet")]) == 1
