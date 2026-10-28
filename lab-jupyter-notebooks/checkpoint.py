"""Checkpoint: does tasting.ipynb run from a clean start, and are both notebooks ready for Git?

    python checkpoint.py

Run it in the lab's terminal, inside (.venv), after the three tasks. It prints CHECKPOINT OK, or what is wrong.
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def fail(message: str) -> None:
    print(f"NOT YET: {message}")
    raise SystemExit(1)


# checked before nbformat is imported: outside the .venv there is no nbformat to import
if sys.prefix == sys.base_prefix:
    fail("this terminal is not inside the lab's .venv - run .venv\\Scripts\\Activate.ps1 first")
if sys.version_info[:2] != (3, 12):
    fail(f"this .venv runs Python {sys.version.split()[0]}; the lab needs 3.12")

import nbformat  # noqa: E402

# 1. Task 2's test: every cell on a brand-new kernel, with no editor - into a temporary folder, so nothing is left behind
with tempfile.TemporaryDirectory() as out:
    run = subprocess.run(
        [sys.executable, "-m", "nbconvert", "--to", "notebook", "--execute", "tasting.ipynb", "--output-dir", out],
        capture_output=True,
        text=True,
    )
    if run.returncode != 0:
        lines = re.sub(r"\x1b\[[0-9;]*m", "", run.stderr).strip().splitlines()  # without the terminal's colours
        fail(f"nbconvert exited with {run.returncode} ({lines[-1] if lines else 'no message'})"
             " - put the salt cell back (task 2) and save the notebook")
    # in another folder, nbconvert keeps the notebook's own name
    ran = nbformat.read(Path(out) / "tasting.ipynb", as_version=4)

results = {}
for cell in ran.cells:
    if cell.cell_type == "code":
        for output in cell.outputs:
            if output.output_type == "execute_result":
                results[cell.source.splitlines()[-1].strip()] = output.data["text/plain"]
for name in ("total_salt", "average"):
    if name not in results:
        fail(f"the run gave no {name} - is its cell still the notebook's own?")

# 2. Rule one: commit the recipe, not the photos of the plate
for name in ("tasting.ipynb", "soup.ipynb"):
    notebook = nbformat.read(name, as_version=4)
    dirty = [c for c in notebook.cells if c.cell_type == "code" and (c.outputs or c.execution_count is not None)]
    if dirty:
        fail(f"{name} still holds outputs or run counts in {len(dirty)} cell(s) - Clear All Outputs, then Ctrl+S")

# 3. Rules two and three: the pantry and Jupyter's hidden copies stay out of Git
for path in (".venv", ".ipynb_checkpoints/tasting-checkpoint.ipynb"):
    if subprocess.run(["git", "check-ignore", "-q", path]).returncode != 0:
        fail(f"Git does not ignore {path.split('/')[0]} - this folder's .gitignore needs its line back")

print(f"tasting.ipynb runs from a clean start: total_salt {results['total_salt']}, average {results['average']}")
print("tasting.ipynb and soup.ipynb hold no outputs; .venv and .ipynb_checkpoints are ignored")
print("CHECKPOINT OK")
