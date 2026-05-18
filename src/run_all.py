import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "water_routing.py",
    "student_assignment.py",
    "eoq.py",
    "simplex_method.py",
    "make_figures.py",
]

for script in SCRIPTS:
    print("\n===", script, "===")
    subprocess.run([sys.executable, str(ROOT / "src" / script)], check=True)
