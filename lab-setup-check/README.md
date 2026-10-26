# Lab · Check your setup

**Last verified:** 2026-10-25 · Python 3.12.10 · numpy 2.5.3 · VS Code 1.142.0 · Python extension 2026.10.0 · Python Environments 1.40.0 · Git 2.52 · Windows 11

**Goal:** you run the kitchen check, a small program that tests a lab's station: Python 3.12, the lab's own `.venv`
and the libraries on its shopping list. You watch it fail with no station, build the station with
**Python: Create Environment** until it prints `CHECKPOINT OK`, then throw the station away and build it again.
This is the routine of every Python lab in the course.

**Time:** about 15 minutes.

## Prerequisites

| You need | Why | Get it |
|---|---|---|
| VS Code with the **Python** extension | the editor, its terminal, and the command that builds a lab's `.venv` | [Set up your machine](../SETUP.md), sections 1 and 4 |
| Python 3.12 | every lab's version | [Set up your machine](../SETUP.md), section 2 |
| Git and the labs cloned | to get this folder | [Set up your machine](../SETUP.md), section 3 and *Run a lab in VS Code* steps 1–2 |

**Cost:** free. Nothing runs in Azure.

## What is in this folder

```
lab-setup-check/
  kitchen_check.py      the kitchen check: tests Python 3.12, the lab's .venv and every library in requirements.txt
  requirements.txt      the shopping list: one library, numpy, pinned to the version the lab was tested with
```

## Steps

### 1. Open the lab's folder — and nothing more yet

Step 3 of [Run a lab in VS Code](../SETUP.md#run-a-lab-in-vs-code), for this lab:

1. Press `Ctrl+K`, then `Ctrl+O` (or the **File** menu, **Open Folder**).
2. Go into `mlops-from-zero`, select the `lab-setup-check` folder and click **Select Folder**.
3. If VS Code asks about a Git repository in a parent folder, choose **Yes**.

⚠️ Do **not** create the environment yet. In this lab, you skip step 4 on purpose first.

### 2. Task 1 · Run the lab with no station

1. Open a terminal: `` Ctrl+Shift+` ``. The prompt ends with `lab-setup-check>` and has no `(.venv)` in front.
2. Run the lab's command:

   ```
   python kitchen_check.py
   ```

   ```
   Kitchen check: is this lab's station ready?
     Python 3.12         WRONG    3.11.9
     the lab's .venv     MISSING  running outside the lab
     numpy 2.5.3         WRONG    2.4.6
   CHECKPOINT FAILED: create this lab's .venv, then run the check again.
   ```

   The program ran on the computer's global Python, the one that the whole computer shares. The `.venv` line and the
   last line are the same on every computer. The Python line and the numpy line show what *your* computer already
   has, so yours may differ (for example `numpy 2.5.3  MISSING  not installed`).
3. Ask for the command's exit code:

   ```
   $LASTEXITCODE
   ```

   ```
   1
   ```

   `1` means it failed. A pipeline step that gets an exit code other than `0` fails the build. The workflow that
   re-checks this lab every month reads the same code.
4. Now run the same check with the right Python, the global Python 3.12:

   ```
   py -V:3.12 kitchen_check.py
   ```

   ```
   Kitchen check: is this lab's station ready?
     Python 3.12         OK       3.12.10
     the lab's .venv     MISSING  running outside the lab
     numpy 2.5.3         MISSING  not installed
   CHECKPOINT FAILED: create this lab's .venv, then run the check again.
   ```

Answer before you open the answers:

- The Python line is OK now. Why does the check still fail?
- Why is it a bad idea to fix the numpy line with `py -V:3.12 -m pip install numpy==2.5.3`?

<details><summary>Answers</summary>

- The right Python is only one of three things. The lab also needs its own station (`.venv`) and the libraries on its
  shopping list, inside that station. A fresh Python 3.12 has neither.
- That command installs numpy into the global Python 3.12, which every lab shares. The next lab that needs another
  numpy version changes it again, and one of the two labs breaks with no message that tells you why. Each lab keeps
  its libraries in its own `.venv`.
</details>

### 3. Task 2 · Build the station, then taste

Step 4 of [Run a lab in VS Code](../SETUP.md#run-a-lab-in-vs-code):

1. Press `Ctrl+Shift+P`, type **Python: Create Environment** and press **Enter**.
2. Choose **Venv**.
3. Choose **Python 3.12** — pick it even if a newer Python is preselected.
4. Tick `requirements.txt` and click **OK**.

   VS Code creates a `.venv` folder inside the lab, installs numpy 2.5.3 into it, and selects it. Wait until the
   message in the bottom-right corner says that the environment is selected.

Step 5, run it:

5. Open a **new** terminal: `` Ctrl+Shift+` ``. This time, VS Code steps into the station for you. The prompt starts
   with `(.venv)`.
6. Run the same command as in Task 1:

   ```
   python kitchen_check.py
   ```

   ```
   Kitchen check: is this lab's station ready?
     Python 3.12         OK       3.12.10
     the lab's .venv     OK       in use
     numpy 2.5.3         OK       2.5.3
   CHECKPOINT OK
   ```

   The command and the code are the same as in Task 1. Only the station changed.
7. Ask where numpy lives now:

   ```
   python -c "import numpy, pathlib; print(pathlib.Path(numpy.__file__).relative_to(pathlib.Path.cwd()))"
   ```

   ```
   .venv\Lib\site-packages\numpy\__init__.py
   ```

   Inside the lab's own `.venv`, and nowhere else. Your global Python is untouched.
8. The `.venv` folder is about 70 MB. Ask Git why it does not list it as a new file:

   ```
   git check-ignore -v .venv
   ```

   ```
   .gitignore:1:.venv/	.venv
   ```

   Line 1 of the repository's `.gitignore` keeps every lab's `.venv` out of Git. A `.venv` is never shared:
   `requirements.txt` is, and anyone can rebuild the same station from it.

### 4. Task 3 · Throw the station away, and build it again

1. In the terminal, step out of the station:

   ```
   deactivate
   ```

   The `(.venv)` in front of the prompt is gone.
2. Delete the station:

   ```
   Remove-Item -Recurse -Force .venv
   ```

   No output. The `.venv` folder is gone from the Explorer.
3. Run the check again:

   ```
   python kitchen_check.py
   ```

   ```
   Kitchen check: is this lab's station ready?
     Python 3.12         WRONG    3.11.9
     the lab's .venv     MISSING  running outside the lab
     numpy 2.5.3         WRONG    2.4.6
   CHECKPOINT FAILED: create this lab's .venv, then run the check again.
   ```

   The same failure as in Task 1 (your Python and numpy lines may differ, as before).
4. Build the station again: press `Ctrl+Shift+P`, type **Python: Create Environment** and press **Enter**.
5. Choose **Venv**.
6. Choose **Python 3.12**.
7. Tick `requirements.txt` and click **OK**. Wait until the message in the corner says that the environment is
   selected.
8. Open a **new** terminal: `` Ctrl+Shift+` ``. The prompt starts with `(.venv)` again.

Answer before you open the answers:

- What changed on your computer, outside this lab's folder, when you deleted `.venv`?
- Why is the new station the same as the old one?

<details><summary>Answers</summary>

- Nothing. The station lives only in the lab's folder, so nothing else on your computer notices it is gone.
- `requirements.txt` pins the exact version, `numpy==2.5.3`, and you chose the same Python, 3.12. The same shopping
  list in the same kind of kitchen gives the same station, today or in a year.
</details>

## Checkpoint

In the terminal (its prompt starts with `(.venv)`):

```
python kitchen_check.py
```

```
Kitchen check: is this lab's station ready?
  Python 3.12         OK       3.12.10
  the lab's .venv     OK       in use
  numpy 2.5.3         OK       2.5.3
CHECKPOINT OK
```

`CHECKPOINT OK` means: the program runs on Python 3.12, inside this lab's own `.venv`, and every library on the
shopping list is installed there at its pinned version. Anything else prints `CHECKPOINT FAILED`, with `WRONG` or
`MISSING` on the line that needs fixing, and the exit code is `1`.

## Stretch (optional)

Change the shopping list on purpose. In `requirements.txt`, change `numpy==2.5.3` to `numpy==2.4.6` and press `Ctrl+S`.
Run `python kitchen_check.py`: the numpy line now says `numpy 2.4.6  WRONG  2.5.3`. Bring the station in line with the
list:

```
python -m pip install -r requirements.txt
```

```
Collecting numpy==2.4.6 (from -r requirements.txt (line 1))
...
Successfully installed numpy-2.4.6
```

The check passes again: it tests the station against the list, whatever the list says. Change the line back to
`numpy==2.5.3`, save, and run the same `pip install` and the check once more.

## If it breaks

- **`python` opens the Microsoft Store, or is "not recognized":** see *If something here breaks* in
  [Set up your machine](../SETUP.md#if-something-here-breaks). For Task 1 you can use `py -V:3.12 kitchen_check.py`
  alone.
- **Python: Create Environment does not offer Python 3.12:** Python 3.12 is not installed yet. Install it
  ([Set up your machine](../SETUP.md), section 2), then close VS Code, open it again, and repeat the step.
- **The prompt starts with `(.venv)`, but the numpy line says `MISSING`:** `requirements.txt` was not ticked. In that
  terminal, run `python -m pip install -r requirements.txt`, then the check again.
- **The `.venv` line says `MISSING` in a terminal with `(.venv)`:** the `.venv` was deleted while this terminal was
  still inside it, or VS Code selected another Python. Open a new terminal; if the prompt has no `(.venv)`, press
  `Ctrl+Shift+P`, run **Python: Select Interpreter**, choose the one in `.venv`, and open a new terminal again.
- **`deactivate` is "not recognized":** this terminal was never inside the station. Go on with the next step.
- **`Remove-Item` says a file is being used by another process:** close every terminal (the bin icon on the
  terminal panel), then run the command in a new terminal.
- **pip says that it cannot find `numpy==2.5.3`:** a newer Python or a moved package can cause this.
  [Open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues) with the step number and the exact output,
  so that the lab gets updated.

## Hand in

Nothing to commit: the lab changes no file that Git tracks, and Git ignores the `.venv`. Check it:

```
git status --short
```

No output means there is nothing to commit. Keep the routine: open the lab's folder, build its station, run it to
`CHECKPOINT OK`.
