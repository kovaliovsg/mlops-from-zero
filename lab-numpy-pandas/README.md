# Lab · NumPy and pandas

**Last verified:** 2026-10-14 · Python 3.12.10 · numpy 2.5.3 · pandas 3.0.6 · pyarrow 25.0.1 · holidays 0.106 · ipykernel 7.4.0 · Windows 11

**Goal:** you run the video's stock-take on almost four years of a restaurant chain's order books, then hunt and
clean with your own cells: you point at rows by label and by position, find blanks, copies, impossible numbers and
messy names with masks, and save a clean table as Parquet that reads back exactly as you wrote it.

**Time:** about 15 minutes.

## Prerequisites

| You need | Why | Get it |
|---|---|---|
| VS Code with the **Python** and **Jupyter** extensions | the editor, its terminal and its notebooks | [Set up your machine](../SETUP.md), sections 1 and 4 |
| Python 3.12 | every lab's version | [Set up your machine](../SETUP.md), section 2 |
| Git and the labs cloned | to get this folder and save your work | [Set up your machine](../SETUP.md), section 3 and *Run a lab in VS Code* steps 1–2 |

**Cost:** free. Nothing runs in Azure.

## What is in this folder

```
lab-numpy-pandas/
  requirements.txt      the libraries, every version pinned to what the video ran
  arrays.py             step 2: NumPy's arrays - one dtype, maths without a loop, a slice that is a view
  generate.py           step 3: writes the order books into data/, with 486 mistakes planted in them
  stock_take.ipynb      steps 4-6: the video's notebook - load, point, hunt, clean, save
  checkpoint.py         the checkpoint
  data/                 made in step 3 and step 6, never committed (.gitignore)
```

## Steps

### 1. Open the lab and build its environment

Steps 3–5 of [Run a lab in VS Code](../SETUP.md#run-a-lab-in-vs-code), for this lab:

1. Press `Ctrl+K`, then `Ctrl+O` (or the **File** menu, **Open Folder**).
2. Go into `mlops-from-zero`, select the `lab-numpy-pandas` folder and click **Select Folder**.
3. Press `Ctrl+Shift+P`, type **Python: Create Environment** and press **Enter**.
4. Choose **Venv**.
5. Choose **Python 3.12** — pick it even if a newer Python is preselected.
6. Tick `requirements.txt` and click **OK**. VS Code creates `.venv` and installs the five pinned libraries with
   everything they need.
7. Open the terminal: `` Ctrl+Shift+` ``. Its prompt starts with `(.venv)`.
8. Prove the terminal's Python is the lab's own — `True` means you are inside `.venv`:

   ```
   python -c "import sys; print(sys.prefix != sys.base_prefix, sys.version.split()[0])"
   ```

   ```
   True 3.12.10
   ```

### 2. NumPy: one array, one dtype, no loop

```
python arrays.py
```

```
int64 (7,)
[252 210 238 266 336 378 294]
20.142857142857142
['18' 'pizza']
(2, 7)
[30 26 30 31 40 46 35]
[141  97]
[18 15 17 19 24  0 21]
```

Line by line, as in the video: a week of pizza sales is one array of `int64`, seven long; `week * 14` multiplies
every day at once, with no loop; one string turns the whole array into text; two branches make a 2 × 7 array, summed
down (`axis=0`, each day) and across (`axis=1`, each branch). The last line is the trap: the script set Saturday to `0`
in `weekend = week[5:7]` only, yet the *week* changed. A slice is a view onto the same numbers, not a copy.

### 3. Write the order books

```
python generate.py
```

```
INFO __main__: wrote 164400 order rows for 1369 days to data
INFO __main__: planted 486 mistakes for you to find
```

`data\` now holds `orders.csv` (about 8 MB: one row per day, branch, service and dish, from 2023-01-01 to
2026-09-30), `dishes.csv` (the menu: 12 dishes), `branches.csv` and `weather.csv`. The seed is fixed at 42, so your
files are byte for byte the ones in the video.

### 4. Run the video's stock-take

1. Open `stock_take.ipynb` (`Ctrl+P`, type `stock_take.ipynb`, press **Enter**).
2. Click the kernel picker in the notebook's top right (or press `Ctrl+Shift+P`, type
   **Notebook: Select Notebook Kernel** and press **Enter**).
3. Choose **Python Environments** (if you see **Select Another Kernel** first, choose that, then
   **Python Environments**).
4. Choose `.venv` (Python 3.12.10).
5. Click **Run All** on the notebook toolbar.

Every cell gets a green tick. VS Code shows the tables as grids; the numbers are the ones below. The cells that
matter for the tasks:

| Cell | Output |
|---|---|
| `orders.shape` | `(164400, 6)` |
| `orders.isna().sum()` | `branch 25`, `qty 80`, every other column `0` |
| `orders.describe()` | `min -20.000000`, `max 1300.000000` |
| `orders.loc[0:2]` | 3 rows: `0`, `1`, `2` |
| `orders.iloc[0:2]` | 2 rows: `0`, `1` |
| `refund.sum()` | `np.int64(15)` |
| `orders[orders["qty"] > 500]` | 6 rows, from `600.0` to `1300.0` |
| `orders.duplicated().sum()` | `np.int64(120)` |
| `orders["dish"].nunique()` | `36` |
| `(~orders["dish"].isin(menu)).sum()` | `np.int64(200)` |
| `len(orders) - len(clean)` | `246` |
| `clean["dish"].isin(menu).all()` | `np.True_` |
| the last cell | `date str`, `branch str`, `service str`, `dish str`, `qty float64`, `promo bool` |

### 5. Task 1 · Read the table, point at its rows

Answer from the outputs of step 4 before you open the answers:

- How many rows and columns does `orders` have?
- Which two columns have blanks, and how many each? Which cell tells you, and which other cell tells you too?
- What are the smallest and the largest `qty`? Why are both impossible?
- `orders.loc[0:2]` and `orders.iloc[0:2]` ask for "0 to 2". Why does one give three rows and the other two?

<details><summary>Answers</summary>

- 164,400 rows, 6 columns: `(164400, 6)`.
- `branch` (25) and `qty` (80): `isna().sum()` counts them; `info()` shows them too, as a *Non-Null Count* below
  164400 (`164375` and `164320`).
- `min` is `-20` and `max` is `1300`: nobody sells minus twenty portions — a refund typed as a sale — and 1,300
  portions of one dish at one service is two zeros too many at the till.
- `loc` points by **label** and includes both ends: labels 0, 1 and 2. `iloc` points by **position** and stops
  before the end, like a Python list slice: positions 0 and 1.
</details>

### 6. Task 2 · Hunt with your own masks

Add a cell under the notebook's last one (hover below it and click **+ Code**), paste each snippet into its own cell
and run it with `Shift+Enter`. Guess the answer first.

1. How many refunds were rung up on a promotion? `&` keeps the rows where **both** masks are `True`:

   ```python
   (refund & orders["promo"]).sum()
   ```

   ```
   np.int64(1)
   ```

2. Which branches lost a quantity? `loc` takes a mask for the rows and a column name for the column:

   ```python
   orders.loc[orders["qty"].isna(), "branch"].value_counts()
   ```

   ```
   branch
   Downtown     20
   Riverside    19
   Harbor       15
   Airport      15
   Uptown       11
   Name: count, dtype: int64
   ```

   20 + 19 + 15 + 15 + 11 = 80, the blank quantities `isna()` counted.
3. The clean-up repairs dish names with `.str.strip().str.title()`. Is one of the two enough? Count the names still
   off the menu after each one alone (`~` flips the mask: `True` for every name that is **not** on the menu):

   ```python
   (~orders["dish"].str.strip().isin(menu)).sum()
   ```

   ```
   np.int64(200)
   ```

   ```python
   (~orders["dish"].str.title().isin(menu)).sum()
   ```

   ```
   np.int64(100)
   ```

   <details><summary>Why</summary>

   The 200 messy names come in two kinds: 100 in capitals (`MINESTRONE`) and 100 in lower case with a space at each
   end (` greek salad `). `strip()` alone removes the spaces but leaves both kinds in the wrong case: still 200 off
   the menu. `title()` alone fixes the capitals but keeps the spaces: still 100 off. Only both together bring every
   name back to the menu's own spelling — which is why `clean["dish"].isin(menu).all()` says `np.True_`.
   </details>

### 7. Task 3 · Clean, save, and read it back

The notebook's clean-up dropped 246 rows. Check the clean table, then the file it wrote. One snippet per cell, as in
Task 2.

1. Does 246 add up? The planted mistakes it drops are 120 copies, 25 rows with no branch, 80 with no quantity, 15
   refunds and 6 typed with two zeros too many:

   ```python
   120 + 25 + 80 + 15 + 6
   ```

   ```
   246
   ```

   (The 200 messy names were repaired, not dropped. The 40 impossible dates, like `2023-02-30`, are still in: this
   clean-up does not check dates.)
2. Nothing left to find:

   ```python
   clean.duplicated().sum()
   ```

   ```
   np.int64(0)
   ```

   ```python
   clean[["branch", "qty"]].isna().sum()
   ```

   ```
   branch    0
   qty       0
   dtype: int64
   ```

3. Point at "7677 to 7679" by label and by position in `clean`, the table with rows dropped:

   ```python
   clean.loc[7677:7679]
   ```

   ```
               date  branch service         dish  qty  promo
   7677  2023-03-05  Uptown   lunch  Greek Salad  1.0  False
   7679  2023-03-05  Uptown   lunch      Lasagna  4.0  False
   ```

   ```python
   clean.iloc[7677:7679]
   ```

   ```
               date   branch service             dish   qty  promo
   7693  2023-03-06  Airport  dinner       Minestrone   5.0  False
   7694  2023-03-06  Airport  dinner  Pepperoni Pizza  17.0  False
   ```

   <details><summary>Why</summary>

   Dropping rows keeps the labels of the rows that stay. Label 7678 was a row with no branch (you saw it in step 4,
   under `orders[orders["branch"].isna()]`), so `loc` finds only 7677 and 7679. `iloc` counts positions: 16 rows were
   dropped before this point, so position 7677 now holds the row labelled 7693.
   </details>

4. Read the Parquet file back:

   ```python
   back = pd.read_parquet("data/orders.parquet")
   back.shape
   ```

   ```
   (164154, 6)
   ```

   ```python
   back.loc[7677:7679, ["branch", "qty"]]
   ```

   ```
          branch   qty
   7677  Airport   5.0
   7678  Airport  17.0
   7679  Airport   0.0
   ```

   The file was saved with `index=False`, so the old labels did not come along: reading it back numbers the rows 0,
   1, 2, … again, and label 7677 is the row that sat at position 7677. The dtypes came back exactly as written — the
   notebook's last cell showed them.

## Checkpoint

In the terminal (its prompt starts with `(.venv)`):

```
python checkpoint.py
```

```
orders.parquet: 164,154 rows, 5 branches, 12 dishes
dropped 246 rows; blanks 0, copies 0, qty from 0 to 41
CHECKPOINT OK
```

`CHECKPOINT OK` means: you are inside the lab's own environment with Python 3.12, and `data\orders.parquet` is the
clean order book — no copies, no blanks in `branch` or `qty`, every quantity from 0 to 500, every dish on the menu,
the dtypes kept, and exactly the 246 planted rows gone. Anything else prints `NOT YET:` and what to fix.

## Stretch (optional)

- In `arrays.py`, change `weekend = week[5:7]` to `weekend = week[5:7].copy()` and run it again. Which line of the
  output changes, and why? Change it back.
- Write the clean table once more without `index=False` — `clean.to_parquet("data/with-index.parquet")` — and read
  it back with `pd.read_parquet`. What happened to the row labels?

## If it breaks

- **`python` opens the Microsoft Store, or `py` is not recognized:** see
  [If something here breaks](../SETUP.md#if-something-here-breaks) on the setup page.
- **`checkpoint.py` says `not inside the lab's .venv`:** the terminal was opened before the environment existed.
  Close it (the bin icon), open a new one with `` Ctrl+Shift+` ``; the prompt must start with `(.venv)`. Or run
  `.venv\Scripts\Activate.ps1` in this folder (if PowerShell refuses to run scripts, run
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once first).
- **The kernel list has no `.venv`:** step 1 did not finish. Run **Python: Create Environment** again, then pick the
  kernel again.
- **`FileNotFoundError: data/orders.csv`:** run `python generate.py` in this folder first (step 3).
- **Creating the environment fails because a pinned version is gone:** the libraries moved on. Remove the `==…`
  pins from `requirements.txt`, install again, and
  [open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues) so this lab gets re-pinned. If your numbers
  then differ from the ones above, say so in the issue.

## Hand in

Commit your answers to the three tasks, as `lab-numpy-pandas/my-answers.md`, to your fork. `data\` stays out of Git
(this folder's `.gitignore`): it is rebuilt from `generate.py` and its seed, never shared.
