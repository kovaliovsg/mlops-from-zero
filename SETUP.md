# Set up your machine — do this once, before your first lab

**Last checked:** 2026-10-06 · Windows · VS Code 1.126 · Python 3.12.10 · Git 2.54 · Docker 29.8

You work every lab in this course **from your own computer, in VS Code** — even the later labs that create
resources in Azure are driven from here. Installing and running a real toolchain is part of the job, so there is no
"click here and it runs in the cloud" shortcut. This page lists every tool the labs use,
where to get it, and the few install choices that matter. It grows as the course grows: a tool appears here when the
first lab that needs it is published.

The steps are written for **Windows**, the platform the course uses. On macOS or Linux, use the same download pages;
the commands that differ are noted.

## What each lab needs

| Tool | Spot the drift | The first brick | A model in a box |
|---|---|---|---|
| [VS Code](#1-vs-code) + the [Python extension](#4-the-python-extension-in-vs-code) | ✅ | ✅ | ✅ |
| [Python 3.12](#2-python-312) | ✅ | ✅ | — (Python runs inside the container) |
| [Git](#3-git) | ✅ | ✅ | ✅ |
| [Docker Desktop](#5-docker-desktop) | — | — | ✅ |

## 1. VS Code

The editor for everything in this course: code, terminal, notebooks, Git.

- **Get it:** https://code.visualstudio.com/download → **Windows** → **User Installer, x64**.
- **Install:** accept the defaults. Setup adds VS Code to your PATH, so open a **new** terminal afterwards.
- **Check:**

  ```
  code --version
  ```

  The first line is the version, for example `1.126.0`.

## 2. Python 3.12

Every lab uses Python **3.12** — the version the course's libraries and Azure Machine Learning are verified with.

- **Get it:** https://www.python.org/downloads/windows/ → **Python install manager** (the way python.org recommends
  installing Python on Windows today), or from a terminal: `winget install 9NQ7512CXL7T`.
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

Only for *A model in a box*.

- **Get it:** https://www.docker.com/products/docker-desktop/ → **Download for Windows**.
- **Install:** accept the defaults. It uses **WSL 2**; the installer sets it up and may ask for a restart.
- **Check:** start Docker Desktop, wait until it says it is running, then:

  ```
  docker run --rm hello-world
  ```

  Expected output contains `Hello from Docker!`.

## Run a lab in VS Code

[![Run a lab in VS Code - how to set up and run a lab (YouTube video)](assets/video-run-a-lab-in-vs-code.jpg)](https://youtu.be/g1SpgAq6Zqc)

**Video: [Run a lab in VS Code](https://youtu.be/g1SpgAq6Zqc)** (12 min) — these steps, recorded for real. Click the picture to watch it on YouTube.

Two steps you do **once**, three you do for **every lab**.

**Once, on day one**

1. **Install the Python extension** ([section 4](#4-the-python-extension-in-vs-code)).
2. **Get the labs:** in VS Code, `Ctrl+Shift+P` → **Git: Clone** → paste
   `https://github.com/kovaliovsg/mlops-from-zero.git` → choose a folder → **Open**.
   (Or fork the repository first and clone your fork — your fork becomes your public project.)
   If VS Code asks whether you trust the authors, choose **Yes, I trust the authors** (on a Restricted Mode banner,
   **Manage** → **Trust**; check any time with **Workspaces: Manage Workspace Trust**): trusting the `mlops-from-zero` folder trusts every lab inside it.

**For every lab** (a lab that runs in a container, like *A model in a box*, needs no `.venv`: after step 3 follow
its README)

3. **Open the lab's folder:** **File → Open Folder** (`Ctrl+K` `Ctrl+O`) → `mlops-from-zero\<lab folder>` — the
   lab's own folder, not the whole repository.
   If VS Code asks about a Git repository in a parent folder, choose **Yes**: that lets **Git: Pull** work from
   the lab's window.
4. **Create its environment:** `Ctrl+Shift+P` → **Python: Create Environment** → **Venv** → **Python 3.12** (pick it
   even if a newer Python is preselected) → tick `requirements.txt` if the lab has one → **OK**. VS Code creates
   `.venv`, installs the libraries and selects it.
5. **Run it:** open the terminal (`` Ctrl+Shift+` ``); its prompt starts with `(.venv)`. Follow the lab's README from
   its first step; the **Checkpoint** at the end proves it worked.

**A new lab was published?** Don't clone again: `Ctrl+Shift+P` → **Git: Pull** brings it into your copy. On a fork,
first press **Sync fork** on your fork's GitHub page, then **Git: Pull**.
Cloned the original and want a fork now? Fork it on GitHub, then clone your fork into a new folder.

## If something here breaks

- **`py` or `python` opens the Microsoft Store:** Python is not installed yet, or its command aliases are not set.
  Install the Python install manager above; then open **Start → Manage app execution aliases** and check that the
  **Python (default)** aliases are on (`python.exe` set to *Python (default)*). If they already are, turn them off and
  on again. ([Python docs](https://docs.python.org/3/using/windows.html))
- **`code`, `git` or `py` is "not recognized" right after installing:** open a **new** terminal (or restart VS Code);
  installers change PATH for new windows only.
- **A download page moved:** search for the tool's name plus "download"; then
  [open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues) so this page gets fixed.
