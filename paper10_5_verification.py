"""Run all Paper 10.5 executable verification modules."""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
scripts = [HERE / f'F{i}_{name}.py' for i,name in [
    (25,'beta'), (26,'relay_distance'), (27,'mass_quantum'), (28,'two_transitions'),
    (29,'port_exhaustion'), (30,'single_regime'), (31,'claim_registry')]]

for script in scripts:
    print(f'\n=== {script.name} ===')
    result = subprocess.run([sys.executable, str(script)], text=True, capture_output=True)
    if result.stdout:
        print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, end='', file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(f'FAILED: {script.name}')
print('\nALL PAPER 10.5 VERIFICATION SCRIPTS PASS: 7/7')
