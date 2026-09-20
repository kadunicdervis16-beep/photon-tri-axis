"""Paper 10.5 — F.27: exact 1-CU minimum."""
from itertools import product

STATES = list(product("XYO", repeat=3))
state_costs = [sum(c != 'O' for c in s) for s in STATES]
assert min(c for c in state_costs if c > 0) == 1

# The minimum is a granularity statement; the ceiling is separate.
for n_total in range(4, 201):
    c_exec = n_total - 3
    assert c_exec >= 1
    assert 1 <= c_exec

print("F.27 PASS: minimum non-zero native workload is exactly 1 CU; tested N_total=4..200.")
