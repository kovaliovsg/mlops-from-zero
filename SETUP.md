# Set up your machine — do this once, before your first lab

**Last checked:** 2026-10-06 · Windows · VS Code 1.126 · Python 3.12.10 · Git 2.54

You work every lab in this course **from your own computer, in VS Code** — even the later labs that create
resources in Azure are driven from here. Installing and running a real toolchain is part of the job, so there is no
"click here and it runs in the cloud" shortcut. This page lists every tool the labs use,
where to get it, and the few install choices that matter. It grows as the course grows: a tool appears here when the
first lab that needs it is published.

The steps are written for **Windows**, the platform the course uses. On macOS or Linux, use the same download pages;
the commands that differ are noted.

## What each lab needs

| Tool | Spot the drift |
|---|---|
| [VS Code](#1-vs-code) + the [Python extension](#4-the-python-extension-in-vs-code) | ✅ |
| [Python 3.12](#2-python-312) | ✅ |
| [Git](#3-git) | ✅ |

## 1. VS Code

The editor for everything in this course: code, terminal, notebooks, Git.

- **Get it:** on https://code.visualstudio.com/download, under **Windows**, click **User Installer** **x64**.
- **Install:** accept the defaults. Setup adds VS Code to your PATH, so open a **new** terminal afterwards.
- **Check:**

  ```
  code --version
  ```

  The first line is the version, for example `1.126.0`.

## 2. Python 3.12

Every lab uses Python **3.12** — the version the course's libraries and Azure Machine Learning are verified with.

- **Get it:** on https://www.python.org/downloads/windows/, download the **Python install manager** (the way
  python.org recommends installing Python on Windows today), or from a terminal: `winget install 9NQ7512CXL7T`.
- **Install:** run the downloaded file and accept the defaults. Then, in a new terminal, run the install manager's
  configuration checker and accept its recommended changes:

  ```
  py install --configure -y
  ```
- **Add Python 3.12** (in a new terminal):

  ```
  py install 3.12
  ```

- **Check:**

  ```
  py -V:3.12 --version
  ```

  Expected: `Python 3.12.10` — the last 3.12 release that python.org builds for Windows.
- **macOS:** `brew install python@3.12` · **Ubuntu:** `sudo apt install python3.12 python3.12-venv`.

## 3. Git

To get the labs and to save your own work in your fork.

- **Get it:** https://git-scm.com/downloads/win, or from a terminal: `winget install --id Git.Git -e`.
- **Install:** accept the defaults.
- **Check:**

  ```
  git --version
  ```

  Expected: `git version 2.x…` (any recent version works).

## 4. The Python extension in VS Code

- In VS Code, open **Extensions** (`Ctrl+Shift+X`), search **Python**, and install **Python** published by
  **Microsoft** (`ms-python.python`). It brings **Pylance**, the **Python Debugger** and **Python Environments**
  with it — the last one creates each lab's `.venv`.
- That is all the current labs need. Notebook labs will add the **Jupyter** extension when they arrive.

## 5. Docker Desktop

Only for the lab that puts a model in a container. Its install steps appear here when that lab is published —
skip it until then.

## Run a lab in VS Code

[![Run a lab in VS Code - how to set up and run a lab (YouTube video)](assets/video-run-a-lab-in-vs-code.jpg)](https://youtu.be/g1SpgAq6Zqc)

**Video: [Run a lab in VS Code](https://youtu.be/g1SpgAq6Zqc)** (12 min) — these steps, recorded for real. Click the picture to watch it on YouTube.

Two steps you do **once**, three you do for **every lab**.

**Keyboard shortcuts used below** (on macOS, `Cmd` instead of `Ctrl`):

| Shortcut | What it does |
|---|---|
| `Ctrl+Shift+P` | opens the **Command Palette** — VS Code's search box for every command; type a command's name and press **Enter** |
| `Ctrl+K`, then `Ctrl+O` | **Open Folder** (the same as the **File** menu, **Open Folder**) |
| `` Ctrl+Shift+` `` | opens a **terminal** (`` ` `` is the backtick key, left of `1`) |
| `Ctrl+Shift+X` | opens **Extensions** |

**Once, on day one**

1. **Install the Python extension** ([section 4](#4-the-python-extension-in-vs-code)).
2. **Get the labs:**
   1. Press `Ctrl+Shift+P`, type **Git: Clone** and press **Enter**.
   2. Paste `https://github.com/kovaliovsg/mlops-from-zero.git` and press **Enter**.
   3. Choose the folder to clone into.
   4. When VS Code asks whether to open the cloned repository, click **Open**.
   5. If VS Code asks whether you trust the authors, choose **Yes, I trust the authors**. Trusting the
      `mlops-from-zero` folder trusts every lab inside it. (On a Restricted Mode banner instead, click **Manage**,
      then **Trust**. To check any time: `Ctrl+Shift+P`, **Workspaces: Manage Workspace Trust**.)

   Or fork the repository first and clone your fork — your fork becomes your public project.

**For every lab** (a lab that runs in a container needs no `.venv`: after step 3 follow its README)

3. **Open the lab's folder:**
   1. Press `Ctrl+K`, then `Ctrl+O` (or the **File** menu, **Open Folder**).
   2. Go into `mlops-from-zero`, select the lab's own folder (for example `lab-what-is-mlops`) — not the whole
      repository — and click **Select Folder**.
   3. If VS Code asks about a Git repository in a parent folder, choose **Yes**: that lets **Git: Pull** work from
      the lab's window.
4. **Create its environment:**
   1. Press `Ctrl+Shift+P`, type **Python: Create Environment** and press **Enter**.
   2. Choose **Venv**.
   3. Choose **Python 3.12** — pick it even if a newer Python is preselected.
   4. Tick `requirements.txt` if the lab has one, and click **OK**.

   VS Code creates `.venv`, installs the libraries and selects it.
5. **Run it:**
   1. Open the terminal: `` Ctrl+Shift+` ``. Its prompt starts with `(.venv)`.
   2. Follow the lab's README from its first step; the **Checkpoint** at the end proves it worked.

**A new lab was published?** Don't clone again:
1. On a fork only: press **Sync fork** on your fork's GitHub page.
2. In VS Code, press `Ctrl+Shift+P`, type **Git: Pull** and press **Enter**. The new lab is now in your copy.

Cloned the original and want a fork now? Fork it on GitHub, then clone your fork into a new folder.

## If something here breaks

- **`py install …` says `can't open file '…\install'`:** an older Python on your machine installed the old
  **Python Launcher**, and its `py` command wins over the install manager's. The old launcher does not know
  `install`, so it looks for a script file with that name.
  1. Check the install manager is there: run `pymanager help`. If it is not recognized, install it first (above).
  2. Click **Start**, open **Installed apps**, search **Python launcher** and click **Uninstall**. This removes only
     the old `py` command; any Python you already have stays installed.
  3. Open a **new** terminal and run the `py install` steps again.

  To keep the old launcher instead, type `pymanager` in place of `py` for the install steps
  (`pymanager install --configure -y`, `pymanager install 3.12`).
  ([Python docs](https://docs.python.org/3/using/windows.html#troubleshooting))
- **`py` or `python` opens the Microsoft Store:** Python is not installed yet, or its command aliases are not set.
  Install the Python install manager above; then open **Start**, search **Manage app execution aliases**, and check that the
  **Python (default)** aliases are on (`python.exe` set to *Python (default)*). If they already are, turn them off and
  on again. ([Python docs](https://docs.python.org/3/using/windows.html))
- **`code`, `git` or `py` is "not recognized" right after installing:** open a **new** terminal (or restart VS Code);
  installers change PATH for new windows only.
- **A download page moved:** search for the tool's name plus "download"; then
  [open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues) so this page gets fixed.
