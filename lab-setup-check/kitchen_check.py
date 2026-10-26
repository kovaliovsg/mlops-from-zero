"""The kitchen check - the lab for "Run a lab in VS Code".

Every lab in this course runs in its own station: Python 3.12, the lab's own
.venv folder, and the libraries that its requirements.txt names. This program
checks all three. When all three are right, it prints CHECKPOINT OK.
"""
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

LAB = Path(__file__).resolve().parent


def shopping_list():
    """The libraries and versions that requirements.txt names."""
    wanted = {}
    for line in (LAB / "requirements.txt").read_text().splitlines():
        line = line.split("#")[0].strip()
        if "==" in line:
            name, pinned = line.split("==")
            wanted[name.strip()] = pinned.strip()
    return wanted


def report(label, status, found):
    print(f"  {label:<20}{status:<9}{found}")
    return status == "OK"


print("Kitchen check: is this lab's station ready?")
checks = []

python = ".".join(str(n) for n in sys.version_info[:3])
checks.append(report("Python 3.12", "OK" if sys.version_info[:2] == (3, 12) else "WRONG", python))

inside = Path(sys.prefix).resolve() == (LAB / ".venv").resolve()
checks.append(report("the lab's .venv", "OK" if inside else "MISSING",
                     "in use" if inside else "running outside the lab"))

for name, pinned in shopping_list().items():
    try:
        found = version(name)
    except PackageNotFoundError:
        checks.append(report(f"{name} {pinned}", "MISSING", "not installed"))
        continue
    checks.append(report(f"{name} {pinned}", "OK" if found == pinned else "WRONG", found))

if all(checks):
    print("CHECKPOINT OK")
else:
    print("CHECKPOINT FAILED: create this lab's .venv, then run the check again.")
    sys.exit(1)
