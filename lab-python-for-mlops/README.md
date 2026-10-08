# Lab · Stand up the prep-forecast repo

**[MLOps from Zero](https://www.youtube.com/playlist?list=PLKblUEvSYoDc)** — the video course these labs belong to, every lesson in order (YouTube playlist).

<a href="https://www.youtube.com/playlist?list=PLKblUEvSYoDc"><img src="../assets/course-mlops-from-zero.jpg" width="480" alt="MLOps from Zero - the video course for these labs (YouTube playlist)"></a>

**[Run a lab in VS Code](https://youtu.be/g1SpgAq6Zqc)** — how to set up your machine and run any lab, recorded step by step (YouTube video).

<a href="https://youtu.be/g1SpgAq6Zqc"><img src="../assets/video-run-a-lab-in-vs-code.jpg" width="480" alt="Run a lab in VS Code - how to set up and run a lab (YouTube video)"></a>

**Last verified:** 2026-10-08 · Python 3.12.10 · pip 26.2.1 · pandas 3.0.6 · numpy 2.5.3 · pytest 9.1.1 · Windows 11

**Do this lab after Part 7 in the playlist.**

**Goal:** you stand up the project every later lab builds on — the demand forecast for a five-branch restaurant
chain. You build its pantry by hand and lock it, see why a seed matters, find the mistakes hidden in three years of
order books, turn the notebook's clean-up into a command a pipeline can run, and prove it with tests.

**Time:** about 35 minutes.

## Prerequisites

| You need | Why | Get it |
|---|---|---|
| VS Code with the **Python** and **Jupyter** extensions | the editor, its terminal and its notebooks | [Set up your machine](../SETUP.md), sections 1 and 4 |
| Python 3.12 | every lab's version | [Set up your machine](../SETUP.md), section 2 |
| Git and the labs cloned | to get this folder and save your work | [Set up your machine](../SETUP.md), section 3 and *Run a lab in VS Code* steps 1–2 |

**Cost:** free. Nothing runs in Azure.

## What you will have at the end

```
lab-python-for-mlops/
  pyproject.toml          the recipe card: what the project needs, every version pinned
  pylock.toml             the lock you make in step 1 - the exact pantry, with hashes
  taste_test.py           step 2: the same code, the same data - is the score the same?
  explore.ipynb           step 4: the data scientist's notebook
  src/prep_forecast/      steps 3 and 6: the code, as a package
    generate.py             writes three years of order books, with mistakes planted in them
    cleaning.py             the notebook's clean-up, refactored into functions
    prepare.py              the command a pipeline runs: arguments, a config file, logging, an exit status
  config.toml             prepare's settings - never a password or a key
  tests/                  step 7: what proves the clean-up works
  checkpoint.py           step 8
  data/                   made in steps 3 and 6, never committed (.gitignore)
```

## Steps

### 1. Build the pantry by hand, and lock it

This lab makes its environment the way the video does, in the terminal, so you see every piece.

1. Press `Ctrl+K`, then `Ctrl+O` (or the **File** menu, **Open Folder**).
2. Go into `mlops-from-zero`, select the `lab-python-for-mlops` folder and click **Select Folder**.
3. Open the terminal: `` Ctrl+Shift+` ``.
4. Create the virtual environment with Python 3.12, and step into it:

   ```
   py -V:3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   The prompt now starts with `(.venv)`. (macOS / Linux: `python3.12 -m venv .venv`, then `source .venv/bin/activate`.)
   If VS Code asks whether to select the new environment for this folder, click **Yes**.
5. Prove you are inside it — `True` means this terminal's Python is the lab's own:

   ```
   python -c "import sys; print(sys.prefix != sys.base_prefix, sys.version.split()[0])"
   ```

   ```
   True 3.12.10
   ```

6. Upgrade pip. Python 3.12.10 ships pip 25.0.1, which has no `pip lock` yet:

   ```
   python -m pip install --upgrade pip
   ```

   The last line reads `Successfully installed pip-26.2.1` (or newer).
7. Install the project and its tools, exactly as `pyproject.toml` pins them. `-e` installs it *editable*: the code
   stays in `src\`, and every change you make is live without reinstalling.

   ```
   python -m pip install -e ".[dev]"
   ```

   The last line starts `Successfully installed …` and lists about sixty packages, `pandas-3.0.6` among them.
8. See what is in the pantry now, then lock it:

   ```
   python -m pip freeze --exclude-editable
   python -m pip lock -e ".[dev]"
   ```

   `pip freeze` lists 62 packages, `numpy==2.5.3` and `pandas==3.0.6` among them — what *is* installed.
   `pip lock` writes `pylock.toml`: every package the project resolves to, with the download address and the hash
   of each file, so anyone can check they got the very same files. Open it and look. `pip lock` is still marked
   **experimental**, and the lock is only guaranteed for the Python version and the operating system that made it —
   a lock made on Windows with 3.12 is not a lock for a Linux server.

### 2. The taste test: same code, same data, same score?

Run the model from the video twice, then twice with a seed:

```
python taste_test.py
python taste_test.py
python taste_test.py --seed 42
python taste_test.py --seed 42
```

Expected output (your unseeded scores will differ from these, and from each other):

```
Chef's guess:  off by 3.52 portions a day
Model:         off by 2.63 portions a day   (seed: None)
Chef's guess:  off by 3.52 portions a day
Model:         off by 2.50 portions a day   (seed: None)
Chef's guess:  off by 3.52 portions a day
Model:         off by 2.49 portions a day   (seed: 42)
Chef's guess:  off by 3.52 portions a day
Model:         off by 2.49 portions a day   (seed: 42)
```

Without a seed, the same code on the same data scores differently every run — so a "better" score could be luck.
With a seed, the run repeats exactly. That is why a seed is one of the things written down with every run.

### 3. Generate the order books

```
python -m prep_forecast.generate
```

```
INFO __main__: wrote 164400 order rows for 1369 days to data
INFO __main__: planted 486 mistakes for you to find
```

`data\` now holds `orders.csv` (about 8 MB: one row per day, branch, service and dish, from 2023-01-01 to
2026-09-30), `dishes.csv`, `branches.csv` and `weather.csv`. The same seed always writes the same files.

### 4. Explore it in the notebook

1. Open `explore.ipynb`.
2. Pick its kernel: click the kernel picker in the notebook's top right (or press `Ctrl+Shift+P`, type
   **Notebook: Select Notebook Kernel** and press **Enter**) and choose this lab's `.venv` (Python 3.12.10).
3. Click **Run All** on the notebook toolbar.
4. Read the outputs and answer, before you look below:
   - What are the smallest and the largest `qty` in `describe()`? Why are both impossible?
   - Which two columns have missing values, and how many?
   - The menu has 12 dishes. How many different dish names does `nunique()` find, and why?
   - Which dates did `to_datetime(..., errors="coerce")` refuse?

   <details><summary>Answers</summary>

   - `min` is `-20` and `max` is `1300`: nobody sells minus twenty pizzas, or 1,300 portions of one dish at one
     lunch — a refund typed as a sale, and two zeros too many at the till.
   - `branch` (25) and `qty` (80).
   - 36: the same dishes typed as `MARGHERITA PIZZA` and ` margherita pizza ` count as different names.
   - Days that do not exist, such as `2023-02-30` and `2023-04-31`.
   </details>

5. The last output says **82140** — 5 branches × 12 dishes × 1,369 days. The draft works.
6. Now prove it works from a clean start: click **Restart** on the notebook toolbar, then **Run All** again. A notebook that
   only works because of something you ran earlier, and later deleted, fails here. Same number? Good.

### 5. (Read) Why the notebook is not the product

The notebook found the problems, and that is its job. But it runs only top to bottom, in one window, with nobody
checking it. A pipeline needs a command with inputs, a log and an exit status, and tests that say it still works.
Microsoft's own advice for that move has three steps: **remove what was only for exploring**, **refactor the rest
into functions**, and **test the script in a terminal**. Steps 6 and 7 do exactly that.

### 6. From notebook to command

1. See what a notebook looks like as a plain script:

   ```
   jupyter nbconvert --to script explore.ipynb
   ```

   ```
   [NbConvertApp] Converting notebook explore.ipynb to script
   [NbConvertApp] Writing 2025 bytes to explore.py
   ```

   Open `explore.py`: every cell, in order, with all the exploring still in it — `head()`, `describe()`,
   `value_counts()`. That is the raw material. (A notebook with `%pip` or other `%` lines converts too, but the
   result runs only inside Jupyter until you take those lines out.)
2. Now open `src\prep_forecast\cleaning.py`: the same clean-up, refactored. The exploring is gone; each job is one
   function — `tidy_dish_names`, `clean_orders`, `daily_demand` — that takes a table and gives one back.
3. Open `src\prep_forecast\prepare.py`: the command around them. It reads its settings from `config.toml` with
   `tomllib`, lets the command line override any of them with `argparse`, configures logging once, and ends with an
   exit status. Ask it for help:

   ```
   prepare --help
   ```

   ```
   usage: prepare [-h] [--config CONFIG] [--input INPUT] [--output OUTPUT]
                  [--max-qty MAX_QTY] [--country COUNTRY]
                  [--log-level {DEBUG,INFO,WARNING,ERROR}]

   Clean the order books into daily demand.
   ...
   ```

4. Give it a wrong argument, then ask the terminal how it ended:

   ```
   prepare --max-qty lots
   $LASTEXITCODE
   ```

   ```
   usage: prepare [-h] [--config CONFIG] [--input INPUT] [--output OUTPUT]
                  [--max-qty MAX_QTY] [--country COUNTRY]
                  [--log-level {DEBUG,INFO,WARNING,ERROR}]
   prepare: error: argument --max-qty: invalid int value: 'lots'
   2
   ```

   `2` means "the command line was wrong". A pipeline step that exits with anything but `0` fails the run, so a
   mistake can never slip through as a success. (macOS / Linux: `echo $?`.)
5. Run it for real:

   ```
   prepare
   $LASTEXITCODE
   ```

   ```
   10:55:37 INFO    prep_forecast.cleaning: rows_in          164400
   10:55:37 INFO    prep_forecast.cleaning: duplicate_row       120
   10:55:37 INFO    prep_forecast.cleaning: dish_name_fixed     200
   10:55:37 INFO    prep_forecast.cleaning: bad_date             40
   10:55:37 INFO    prep_forecast.cleaning: missing_branch       25
   10:55:37 INFO    prep_forecast.cleaning: unknown_dish          0
   10:55:37 INFO    prep_forecast.cleaning: missing_qty          80
   10:55:37 INFO    prep_forecast.cleaning: negative_qty         15
   10:55:37 INFO    prep_forecast.cleaning: huge_qty              6
   10:55:37 INFO    prep_forecast.cleaning: rows_out         164114
   10:55:38 INFO    prep_forecast.prepare: wrote 82140 rows (5 branches x 12 dishes x 1369 days) to data\daily_demand.parquet
   0
   ```

   Every one of the 486 planted mistakes is found and counted: 286 rows dropped, 200 dish names repaired.

### 7. Prove it with tests

```
pytest
```

```
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
...
configfile: pyproject.toml
testpaths: tests
collected 16 items

tests\test_cleaning.py ............                                      [ 75%]
tests\test_prepare.py ....                                               [100%]

============================= 16 passed in 0.72s ==============================
```

Open `tests\test_cleaning.py` and `tests\test_prepare.py`. Each test is a plain function with `assert`; the ones
with arguments like `order_books` get them from **fixtures** in `tests\conftest.py`; `@pytest.mark.parametrize`
runs one test on four dish names; `pytest.raises` checks that a menu listing a dish twice is refused; and
`test_a_wrong_argument_exits_with_2` checks the exit status you saw in step 6. pytest found its settings in
`pyproject.toml`, in the `[tool.pytest]` table.

### 8. Commit only what belongs in Git

```
git status --short .
```

```
?? pylock.toml
```

Only your lock file is new. `.venv\`, `data\` and `explore.py` are listed in this folder's `.gitignore`, so they
never reach Git: an environment and generated data are rebuilt from the recipe, never shared.

## Checkpoint

```
python checkpoint.py
```

```
daily_demand.parquet: 82,140 rows, 1,143,986 portions
pytest: 16 passed in 0.71s
CHECKPOINT OK
```

`CHECKPOINT OK` means: you are inside the lab's own environment, the order books exist, `prepare` made exactly one
clean row per day, branch and dish, and every test passes.

## Practice questions

1. Your notebook prints 82,140 on your machine. A colleague opens it, runs it top to bottom, and cell 9 fails with
   `NameError`. What is the most likely cause, and which two clicks would have caught it before you shared it?
2. You run `pip lock` on your Windows laptop with Python 3.12 and commit `pylock.toml`. The team's Linux build server
   runs Python 3.13. Can it rely on your lock?
3. A data scientist hands you a notebook that trains a model. Before it can run unattended — as a scheduled job or a
   pipeline step — Microsoft recommends three changes. Name them, and the Python library that lets the job pass in
   values such as the path to the data.

<details><summary>Answers</summary>

1. Hidden state: cell 9 uses a variable made by a cell you ran earlier and then changed or deleted. The notebook only
   worked because of the order you happened to run things in. **Restart**, then **Run All** — the check in step 4.
2. No. `pip lock` guarantees the lock only for the Python version and the operating system that made it. Make the
   lock where it will be used, or with the same Python on the same platform.
3. Remove the code that was only for exploring, refactor the rest into functions, and test the script in a terminal.
   `argparse` reads the arguments the job passes, such as `--training_data`.
</details>

## Stretch (optional)

- Run `python -m prep_forecast.generate --seed 7`, then `prepare` and `python checkpoint.py`. The mistake counts stay
  the same, but one new line appears in the log: which, and why does the table still have 82,140 rows? (Run
  `python -m prep_forecast.generate` afterwards to get the seed-42 books back.)
- Break the clean-up on purpose: in `cleaning.py`, change `df["qty"] < 0` to `df["qty"] < -5`. Run `pytest`. Which test
  catches it, and what does it print? Change it back.
- Run `$env:PREP_LOG_LEVEL = "WARNING"`, then `prepare`. Where did the log go? (`Remove-Item Env:PREP_LOG_LEVEL` to undo.)

## If it breaks

- **`Activate.ps1 cannot be loaded because running scripts is disabled`:** PowerShell blocks scripts by default. Run
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once, then activate again.
- **`ERROR: unknown command "lock"`:** pip is older than the lock command. Run step 1.6 again inside `(.venv)`.
- **`prepare` or `pytest` is "not recognized":** the terminal is not inside `.venv`. Run `.venv\Scripts\Activate.ps1`
  in this folder; the prompt must start with `(.venv)`.
- **`jupyter nbconvert` wrote `explore.txt` instead of `explore.py`:** the notebook lost its language information. Open
  it, select the `.venv` kernel, **Run All**, save (`Ctrl+S`), and convert again.
- **Creating the environment fails because a pinned version is gone:** the libraries moved on. Remove the `==…` pins
  from `pyproject.toml`, install again, and [open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues)
  so this lab gets re-pinned.

## Hand in

Commit `pylock.toml` and your answers to the practice questions (as `lab-python-for-mlops/my-answers.md`) to your fork.
From the next lab on, the forecast is trained on the table `prepare` writes.
