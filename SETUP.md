# Set up your machine — do this once, before your first lab

**Last checked:** 2026-10-05 · Windows 11 · VS Code 1.126 · Python 3.12.10 · Git 2.54

Every lab in this course runs **on your own computer, in VS Code**. Installing and running a real toolchain is part
of the job, so there is no "click here and it runs in the cloud" shortcut. This page lists every tool the labs use,
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
  **Microsoft** (`ms-python.python`). It brings the **Python Debugger** with it.
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

The same five steps for every lab:

1. **Get the labs:** in VS Code, `Ctrl+Shift+P` → **Git: Clone** → paste
   `https://github.com/kovaliovsg/mlops-from-zero.git` → choose a folder → **Open**.
   (Or fork the repository first and clone your fork — your fork becomes your public project.)
2. **Open the lab's folder:** **File → Open Folder** → `mlops-from-zero\<lab folder>`.
3. **Create its environment:** `Ctrl+Shift+P` → **Python: Create Environment** → **Venv** → **Python 3.12** → tick
   `requirements.txt` if the lab has one. VS Code creates `.venv`, installs the libraries and selects it.
4. **Open the terminal** (`` Ctrl+` ``): it already uses the lab's `.venv` — the prompt starts with `(.venv)`.
5. **Follow the lab's README** from its first step; the **Checkpoint** at the end proves it worked.

## If something here breaks

- **`py` or `python` opens the Microsoft Store:** Python is not installed yet, or the Store alias is in the way —
  install the Python install manager above, or turn the aliases off in *Settings → Apps → Advanced app settings →
  App execution aliases*.
- **`code`, `git` or `py` is "not recognized" right after installing:** open a **new** terminal (or restart VS Code);
  installers change PATH for new windows only.
- **A download page moved:** search for the tool's name plus "download"; then
  [open an issue](https://github.com/kovaliovsg/mlops-from-zero/issues) so this page gets fixed.
