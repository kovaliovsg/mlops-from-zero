# Lab · The first brick

**Last verified:** 2026-10-04 · Python 3.12 · pandas 3.0 · Windows 11, macOS, Ubuntu · VS Code

**For the video:** *Python for MLOps* (this lab is the starting point; it grows when that lesson is produced).

**Goal:** by the end you have Python and pandas working, and you have looked at a real dataset with your
own eyes. That is phase one of the roadmap, and every later lab starts from here.

**You need:** 15 minutes, and VS Code with the Python extension, Python 3.12 and Git — see
[Set up your machine](../SETUP.md). Run every command in the VS Code terminal.

## Steps

### 1. Check whether Python is already there

```bash
py -V:3.12 --version
```

Expected output:

```
Python 3.12.10
```

Not there? Follow [Python 3.12](../SETUP.md#2-python-312) on the setup page, then open a **new** terminal and
run the command again. (macOS / Linux: `python3.12 --version`.)

### 2. Create a folder and a virtual environment

A virtual environment is a private shelf of libraries for one project. You will do this for every lab.

```bash
mkdir mlops-first-brick
cd mlops-first-brick
py -V:3.12 -m venv .venv
```

(macOS / Linux: `python3.12 -m venv .venv`.) Activate it:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows cmd: `.venv\Scripts\activate.bat`
- macOS / Linux: `source .venv/bin/activate`

Your prompt now starts with `(.venv)`.

### 3. Install pandas

```bash
pip install "pandas==3.0.6"
```

Expected output ends with:

```
Successfully installed numpy-... pandas-3.0.6 ...
```

### 4. Load a dataset and look at it

Save this as `first_brick.py` (it downloads the classic penguins dataset, 344 rows):

```python
import pandas as pd

URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
df = pd.read_csv(URL)

print(df.head(10))
print()
print("rows, columns:", df.shape)
print("missing values per column:")
print(df.isna().sum())
```

Run it:

```bash
python first_brick.py
```

Expected output (the first ten rows, then the shape, then the missing-value counts):

```
  species     island  bill_length_mm  bill_depth_mm  flipper_length_mm  body_mass_g     sex
0  Adelie  Torgersen            39.1           18.7              181.0       3750.0    MALE
1  Adelie  Torgersen            39.5           17.4              186.0       3800.0  FEMALE
...
rows, columns: (344, 7)
missing values per column:
species               0
...
```

## Checkpoint

`rows, columns: (344, 7)` printed, and the missing-value table shows a few `NaN` counts above zero.
Those missing values are your first taste of "ingredients that need inspecting".

## Stretch (optional)

Add one line and run it again:

```python
print(df.groupby("species")["body_mass_g"].mean())
```

Which species is heaviest?

## If it breaks

- **`python` opens the Microsoft Store (Windows):** the Store alias is in the way. Run `python3`, or
  disable the alias in *Settings → Apps → Advanced app settings → App execution aliases*.
- **`pip` says the pandas version does not exist:** pandas moved on. Run `pip install pandas` without the
  pin; the lab works with any 3.x. Then open an issue so this file gets updated.
- **The dataset URL returns 404:** the file moved. Any CSV works for this lab; try
  `https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv` and expect `(150, 5)`.

## Hand in

Commit `first_brick.py` to your fork of this repository under `lab-python-for-mlops/`. That is the first
file of your public project.
