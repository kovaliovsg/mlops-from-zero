# Lab · Jupyter notebooks

**[MLOps from Zero](https://www.youtube.com/playlist?list=PLKblUEvSYoDc)** — the video course these labs belong to, every lesson in order (YouTube playlist).

<a href="https://www.youtube.com/playlist?list=PLKblUEvSYoDc"><img src="../assets/course-mlops-from-zero.jpg" width="480" alt="MLOps from Zero - the video course for these labs (YouTube playlist)"></a>

**[Run a lab in VS Code](https://youtu.be/g1SpgAq6Zqc)** — how to set up your machine and run any lab, recorded step by step (YouTube video).

<a href="https://youtu.be/g1SpgAq6Zqc"><img src="../assets/video-run-a-lab-in-vs-code.jpg" width="480" alt="Run a lab in VS Code - how to set up and run a lab (YouTube video)"></a>

**Last verified:** 2026-10-15 · Python 3.12.10 · ipykernel 7.4.0 · nbconvert 7.17.1 · VS Code 1.141.2 · Jupyter extension 2025.9.1 · Git 2.52 · Windows 11

**Do this lab after Part 3 in the playlist.**

**Goal:** you run the video's soup-tasting notebook on the lab's own `.venv`, break it with hidden state and catch the
break twice — with **Restart** and **Run All** in VS Code, and with `jupyter nbconvert --execute` in the terminal and its
exit code — then keep the notebook readable in Git: no outputs, no run counts, no `.venv`.

**Time:** about 15 minutes.

## Prerequisites

| You need | Why | Get it |
|---|---|---|
| VS Code with the **Python** and **Jupyter** extensions | the editor, its terminal and its notebooks | [Set up your machine](../SETUP.md), sections 1 and 4 |
| Python 3.12 | every lab's version | [Set up your machine](../SETUP.md), section 2 |
| Git and the labs cloned | to get this folder, and to see what Git makes of a notebook | [Set up your machine](../SETUP.md), section 3 and *Run a lab in VS Code* steps 1–2 |

**Cost:** free. Nothing runs in Azure.

## What is in this folder

```
lab-jupyter-notebooks/
  requirements.txt      ipykernel and nbconvert, with everything they need, every version pinned to what the video ran
  tasting.ipynb         tasks 1-3: the video's notebook - one week of soup orders and the salt they took
  soup.ipynb            task 3: a one-cell notebook, saved with its output, to read as plain text
  .gitignore            the video's: .venv/ and .ipynb_checkpoints/ stay out of Git
  checkpoint.py         the checkpoint
```

## Steps

### 1. Open the lab and build its environment

Steps 3–5 of [Run a lab in VS Code](../SETUP.md#run-a-lab-in-vs-code), for this lab:

1. Press `Ctrl+K`, then `Ctrl+O` (or the **File** menu, **Open Folder**).
2. Go into `mlops-from-zero`, select the `lab-jupyter-notebooks` folder and click **Select Folder**.
3. If VS Code asks about a Git repository in a parent folder, choose **Yes**. Task 3 needs Git in this window.
4. Press `Ctrl+Shift+P`, type **Python: Create Environment** and press **Enter**.
5. Choose **Venv**.
6. Choose **Python 3.12** — pick it even if a newer Python is preselected.
7. Tick `requirements.txt` and click **OK**. VS Code creates `.venv` and installs the pinned libraries.
8. Open the terminal: `` Ctrl+Shift+` ``. Its prompt starts with `(.venv)`.
9. Prove the terminal's Python is the lab's own — `True` means you are inside `.venv`:

   ```
   python -c "import sys; print(sys.prefix != sys.base_prefix, sys.version.split()[0])"
   ```

   ```
   True 3.12.10
   ```

10. Prove the two packages a notebook needs are in this `.venv`:

    ```
    python -c "import ipykernel, nbconvert; print('ipykernel', ipykernel.__version__, '- nbconvert', nbconvert.__version__)"
    ```

    ```
    ipykernel 7.4.0 - nbconvert 7.17.1
    ```

    **ipykernel** lets this Python run notebook cells as a kernel; **nbconvert** runs a notebook from the terminal
    (task 2). Each `.venv` needs its own copy, once: in the video they were installed with `pip install ipykernel` and
    `pip install nbconvert`; here `requirements.txt` brought both.

### 2. Task 1 · The `.venv` as the kernel, cell by cell

1. Open `tasting.ipynb` (`Ctrl+P`, type `tasting.ipynb`, press **Enter**).
2. Click the kernel picker in the notebook's top right, **Select Kernel** (or press `Ctrl+Shift+P`, type
   **Notebook: Select Notebook Kernel** and press **Enter**).
3. Choose **Python Environments** (if you see **Select Another Kernel** first, choose that, then
   **Python Environments**).
4. Choose `.venv` (Python 3.12.10). The picker now reads `.venv (Python 3.12.10)`; VS Code remembers it for this
   notebook.
5. Click into the first code cell, `orders = [42, 38, 51, 47, 60]`, and press `Ctrl+Enter` (or click the run button on
   the cell's left). A green tick appears under it, and `[1]` beside it.
6. Click into the `salt_per_portion` cell and press `Ctrl+Enter`: `[2]`.
7. Click into the `total_salt` cell and press `Ctrl+Enter`: `[3]`, and under it:

   ```
   357.0
   ```

8. Press `Esc`, then click **Jupyter Variables** on the notebook toolbar. The **Jupyter** panel opens with what the
   kernel holds:

   | Name | Type | Size | Value |
   |---|---|---|---|
   | `orders` | `list` | `5` | `[42, 38, 51, 47, 60]` |
   | `salt_per_portion` | `float` | | `1.5` |
   | `total_salt` | `float` | | `357.0` |

9. Click **Run All** on the notebook toolbar. Every cell runs, top to bottom: `357.0` under `total_salt`, and under the
   last cell:

   ```
   47.6
   ```

Answer before you open the answers:

- After **Run All**, which numbers stand beside the four code cells, and why do they not start at 1?
- `average` is not in the variables table of step 8. Why not? Open **Jupyter Variables** again: is it there now?

<details><summary>Answers</summary>

- `[4]`, `[5]`, `[6]`, `[7]`. The run count counts every run of this kernel, in order. Steps 5–7 used 1, 2 and 3; Run
  All went on from there, because the kernel was never restarted.
- In step 8 its cell had not run yet: the kernel holds only what has run. Run All ran it, so the table now lists
  `average` too, with the value under its cell.
</details>

### 3. Task 2 · Make hidden state, then catch it twice

This is the break your colleague saw in the video. Do it on purpose.

1. Click into the `salt_per_portion` cell, press `Esc`, then press `Delete` (or click the bin icon on the cell's
   toolbar). The cell is gone.
2. Run the `total_salt` cell again (its run button, or click into it and press `Ctrl+Enter`). It still works:
   `[8]`, and

   ```
   357.0
   ```

   The kernel still holds `salt_per_portion` from before. No cell in the file creates it any more: that is
   **hidden state**.
3. Click **Restart** on the notebook toolbar (if VS Code asks whether to restart the kernel, click **Restart**). The
   kernel's memory is now empty.
4. Click **Run All**. The `total_salt` cell fails, and the run stops there:

   ```
   ---------------------------------------------------------------------------
   NameError                                 Traceback (most recent call last)
   Cell In[2], line 1
   ----> 1 total_salt = sum(orders) * salt_per_portion
         2 total_salt

   NameError: name 'salt_per_portion' is not defined
   ```

   The `average` cell below did not run this time: its `47.6` is left over from Task 1.

Now catch the same break with no editor at all — the way a pipeline would.

5. Save the broken notebook: `Ctrl+S`. The command below reads the file on disk, not the editor.
6. In the terminal (prompt `(.venv)`), run every cell on a brand-new kernel:

   ```
   jupyter nbconvert --to notebook --execute tasting.ipynb
   ```

   It prints two warnings first (`RuntimeWarning: Proactor event loop …` and `Kernel is running over TCP without
   encryption`; both are harmless here), then a long traceback that ends with:

   ```
   nbclient.exceptions.CellExecutionError: An error occurred while executing the following cell:
   ------------------
   total_salt = sum(orders) * salt_per_portion
   total_salt
   ------------------


   ---------------------------------------------------------------------------
   NameError                                 Traceback (most recent call last)
   Cell In[2], line 1
   ----> 1 total_salt = sum(orders) * salt_per_portion
         2 total_salt

   NameError: name 'salt_per_portion' is not defined
   ```

7. Ask for the command's exit code:

   ```
   $LASTEXITCODE
   ```

   ```
   1
   ```

   `1` means it failed. A pipeline step that gets a code other than `0` fails the build.
8. Put the salt cell back: click into the `orders` cell, press `Esc`, then `B` (a new code cell below), then
   **Enter**, and type:

   ```python
   salt_per_portion = 1.5  # grams of salt in one portion
   ```

9. Press `Esc`, then `Ctrl+S`.
10. Run the same command again, then the exit code:

    ```
    jupyter nbconvert --to notebook --execute tasting.ipynb
    ```

    ```
    [NbConvertApp] Converting notebook tasting.ipynb to notebook
    ...
    [NbConvertApp] Writing 2829 bytes to tasting.nbconvert.ipynb
    ```

    ```
    $LASTEXITCODE
    ```

    ```
    0
    ```

    No error, and the executed copy is saved next to the notebook as `tasting.nbconvert.ipynb` (the byte count can
    differ by a few bytes on your machine).

### 4. Task 3 · Notebooks in Git

1. Read a notebook as plain text:

   ```
   Get-Content soup.ipynb
   ```

   ```
   {
    "cells": [
     {
      "cell_type": "code",
      "execution_count": 1,
      "id": "b2e0d001",
      "metadata": {},
      "outputs": [
       {
        "data": {
         "text/plain": [
          "238"
         ]
        },
        "execution_count": 1,
        "metadata": {},
        "output_type": "execute_result"
       }
      ],
      "source": [
       "orders = [42, 38, 51, 47, 60]\n",
       "sum(orders)"
      ]
     }
    ],
    "metadata": {
     "kernelspec": {
      "display_name": ".venv",
      "language": "python",
      "name": "python3"
     },
     "language_info": {
      "name": "python",
      "version": "3.12.10"
     }
    },
    "nbformat": 4,
    "nbformat_minor": 5
   }
   ```

   Find the cell's code, its output, its run count (it is stored twice) and the metadata, before you open the
   answers.

   <details><summary>Answers</summary>

   - The code: `"source"`, stored line by line.
   - The output: `"outputs"`, here `"238"`, the result of `sum(orders)` — saved right in the file, like a photo of the
     plate stuck to the recipe.
   - The run count: `"execution_count": 1`, once on the cell and once on its output.
   - The metadata, at the end: which kernel (`.venv`) and which Python (`3.12.10`) made the file.
   </details>

2. Give Git a clean starting point, as the video did before its Git chapter. In `tasting.ipynb`, click **Clear All
   Outputs** on the notebook toolbar, then press `Ctrl+S`. In the terminal, remove Task 2's executed copy and commit
   the notebook:

   ```
   Remove-Item tasting.nbconvert.ipynb
   git add tasting.ipynb
   git commit -q -m "Tasting notebook, outputs cleared"
   ```

   No output: `-q` keeps the commit quiet. (If Git answers `Author identity unknown`, run the two
   `git config --global` lines it prints, with your own name and email, then the commit again.)
3. Now make noise without changing any code. Click **Run All**, wait for the green ticks, press `Ctrl+S`, then ask Git
   what changed:

   ```
   git diff
   ```

   Pages of changes you never made — run counts and outputs. The first ones:

   ```
   -   "execution_count": null,
   +   "execution_count": 3,
       "id": "a1f0c002",
       "metadata": {},
       "outputs": [],
   ```

   ```
   -   "execution_count": null,
   +   "execution_count": 4,
   ```

   Press `Space` for the next page; press `q` to leave. Not one changed line is code.
4. Click **Clear All Outputs**, press `Ctrl+S`, and ask again:

   ```
   git diff
   ```

   Nothing — the noise is gone. (Git may print one line first, `warning: in the working copy of 'tasting.ipynb', LF
   will be replaced by CRLF the next time Git touches it`. It is about line endings, not about your notebook.)
5. Make one real change: in the `orders` cell, change Monday's `42` to `44`. Press `Esc`, then `Ctrl+S`.

   ```
   git --no-pager diff
   ```

   ```
   @@ -17,7 +17,7 @@
       "metadata": {},
       "outputs": [],
       "source": [
   -    "orders = [42, 38, 51, 47, 60]  # soup portions sold, Monday to Friday"
   +    "orders = [44, 38, 51, 47, 60]  # soup portions sold, Monday to Friday"
       ]
      },
      {
   ```

   One real change, one line in the diff.
6. See VS Code's own notebook diff: press `Ctrl+Shift+G` (**Source Control**), then click `tasting.ipynb` under
   **Changes**. It compares the notebook cell by cell and shows the one changed input in its own section.
7. Change `44` back to `42`, press `Esc`, then `Ctrl+S`. `git diff` is empty again.
8. `soup.ipynb` still holds its output. Open it (`Ctrl+P`, type `soup.ipynb`, press **Enter**), click **Clear All
   Outputs**, then press `Ctrl+S`. Ask Git what it sees in this folder:

   ```
   git status --short
   ```

   ```
    M soup.ipynb
   ```

   The cleared notebook, and nothing else: `.venv` is in this folder, yet Git does not list it. Ask why:

   ```
   git check-ignore -v .venv .ipynb_checkpoints/tasting-checkpoint.ipynb
   ```

   ```
   lab-jupyter-notebooks/.gitignore:2:.venv/	.venv
   lab-jupyter-notebooks/.gitignore:4:.ipynb_checkpoints/	.ipynb_checkpoints/tasting-checkpoint.ipynb
   ```

   Line 2 of this folder's `.gitignore` keeps the pantry out; line 4 keeps out the copies that Jupyter and JupyterLab
   save in `.ipynb_checkpoints/` — a teammate may open this folder in them.

## Checkpoint

In the terminal (its prompt starts with `(.venv)`):

```
python checkpoint.py
```

```
tasting.ipynb runs from a clean start: total_salt 357.0, average 47.6
tasting.ipynb and soup.ipynb hold no outputs; .venv and .ipynb_checkpoints are ignored
CHECKPOINT OK
```

`CHECKPOINT OK` means: you are inside the lab's own environment with Python 3.12; `tasting.ipynb` runs top to bottom
on a brand-new kernel (the checkpoint runs the same `nbconvert --execute` as Task 2, into a temporary folder, and its
exit code is `0`); both notebooks are saved with no outputs and no run counts; and Git ignores `.venv` and
`.ipynb_checkpoints`. Anything else prints `NOT YET:` and what to fix — for example, with the salt cell still deleted:

```
NOT YET: nbconvert exited with 1 (NameError: name 'salt_per_portion' is not defined) - put the salt cell back (task 2) and save the notebook
```

## Stretch (optional)

- Run the four code cells out of order: the last cell, then the first, then the third. Which run counts do you get,
  and what would a reader of the saved file believe happened? Finish with **Restart**, then **Run All**.
- Clear a notebook's outputs from the terminal, with no editor — the kind of step a pre-commit check can run:
  `jupyter nbconvert --clear-output --inplace tasting.ipynb`.

## If it breaks

- **`python` opens the Microsoft Store, or `py` is not recognized:** see
  [If something here breaks](../SETUP.md#if-something-here-breaks) on the setup page.
- **The kernel list has no `.venv`:** step 1 did not finish. Run **Python: Create Environment** again, then pick the
  kernel again.
- **VS Code says the kernel needs `ipykernel` and offers to install it:** you picked another Python, not the lab's
  `.venv`. Pick `.venv` (Task 1, steps 2–4); its `ipykernel` is already installed.
- **`jupyter` is not recognized, or `checkpoint.py` says `not inside the lab's .venv`:** the terminal was opened before
  the environment existed. Close it (the bin icon), open a new one with `` Ctrl+Shift+` ``; the prompt must start with
  `(.venv)`. Or run `.venv\Scripts\Activate.ps1` in this folder (if PowerShell refuses to run scripts, run
  `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once first).
- **`$LASTEXITCODE` prints nothing:** it is PowerShell's. In Command Prompt use `echo %ERRORLEVEL%`; on macOS or Linux,
  `echo $?`.
- **`git diff` says `Not a git repository`:** the folder was copied, not cloned. Clone the labs as
  [Run a lab in VS Code](../SETUP.md#run-a-lab-in-vs-code) step 2 shows.
- **Creating the environment fails because a pinned version is gone:** the libraries moved on. Remove the `==…`
  pins from `requirements.txt`, install again, and
  [open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues) so this lab gets re-pinned.

## Hand in

Commit the cleared `soup.ipynb` and your answers to the questions in Tasks 1 and 3, as
`lab-jupyter-notebooks/my-answers.md`, to your fork. `.venv` stays out of Git (this folder's `.gitignore`): it is
rebuilt from `requirements.txt`, never shared.
