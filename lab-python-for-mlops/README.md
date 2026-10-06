# Lab · The first brick

**Last verified:** 2026-10-06 · Python 3.12.10 · pandas 3.0.6 · numpy 2.5.3 · Windows · VS Code

**For the video:** *Python for MLOps* (this lab is the starting point; it grows when that lesson is produced).

**Goal:** by the end you have Python and pandas working, and you have looked at a real dataset with your
own eyes. That is phase one of the roadmap, and every later lab starts from here.

**You need:** 15 minutes, and VS Code with the Python extension, Python 3.12 and the labs cloned — see
[Set up your machine](../SETUP.md) (steps 1–2 of *Run a lab in VS Code*, done once).

## Steps

### 1. Open this lab and create its environment

Follow steps 3–5 of [Run a lab in VS Code](../SETUP.md#run-a-lab-in-vs-code): **File → Open Folder** →
`mlops-from-zero\lab-python-for-mlops`, then **Python: Create Environment** → **Venv** → **Python 3.12** → tick
`requirements.txt` → **OK**. A virtual environment is a private shelf of libraries for one project; VS Code
creates it as `.venv` inside this folder and installs pandas into it.

Open the terminal (`` Ctrl+Shift+` ``). Its prompt starts with `(.venv)`.

### 2. Look at the code

`first_brick.py` downloads the classic penguins dataset (344 rows) and looks at it:

```python
import pandas as pd

URL = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/penguins.csv"
df = pd.read_csv(URL)

print(df.head(10))
print()
print("rows, columns:", df.shape)
print("missing values per column:")
print(df.isna().sum())

ok = df.shape == (344, 7) and df.isna().sum().sum() > 0
print("CHECKPOINT OK" if ok else "CHECKPOINT FAILED")
```

### 3. Run it

```bash
python first_brick.py
```

Expected output (on a narrow terminal pandas hides the middle columns as `...`; a wider one shows them all):

```
  species     island  bill_length_mm  ...  flipper_length_mm  body_mass_g     sex
0  Adelie  Torgersen            39.1  ...              181.0       3750.0    MALE
1  Adelie  Torgersen            39.5  ...              186.0       3800.0  FEMALE
2  Adelie  Torgersen            40.3  ...              195.0       3250.0  FEMALE
3  Adelie  Torgersen             NaN  ...                NaN          NaN     NaN
...

[10 rows x 7 columns]

rows, columns: (344, 7)
missing values per column:
species               0
island                0
bill_length_mm        2
bill_depth_mm         2
flipper_length_mm     2
body_mass_g           2
sex                  11
dtype: int64
CHECKPOINT OK
```

## Checkpoint

`CHECKPOINT OK` printed: the table has 344 rows and 7 columns, and some values are missing (row 3 is almost
empty). Those missing values are your first taste of "ingredients that need inspecting".

## Stretch (optional)

Add one line and run it again:

```python
print(df.groupby("species")["body_mass_g"].mean())
```

Which species is heaviest?

## If it breaks

- **`python` opens the Microsoft Store (Windows):** the command aliases are not set — see
  [If something here breaks](../SETUP.md#if-something-here-breaks) on the setup page.
- **Creating the environment fails because a pinned version does not exist:** the libraries moved on. In the
  terminal run `pip install pandas`; the lab works with any pandas 3.x. Then open an issue so this lab gets re-pinned.
- **The dataset URL returns 404:** the file moved. Open an issue; meanwhile any CSV lets you practise (try
  `https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv`, 150 rows and 5 columns, no missing
  values — so the checkpoint will say FAILED, as it should).

## Hand in

Add your stretch line to `first_brick.py` and commit it to your fork (`lab-python-for-mlops/first_brick.py`).
That is the first file of your public project.
