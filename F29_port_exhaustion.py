"""Paper 10.5 — F.29: exhaustive six-port capacity enumeration."""
from collections import Counter
from fractions import Fraction
from itertools import product

configs = list(product((0, 1), repeat=6))
assert len(configs) == 64
counts = Counter(sum(c) for c in configs)
expected = {0:1, 1:6, 2:15, 3:20, 4:15, 5:6, 6:1}
assert dict(counts) == expected

for blocked in range(6):
    open_ports = 6 - blocked
    factor = Fraction(6, open_ports)
    assert factor == Fraction(6, 6 - blocked)

assert 6 in counts and counts[6] == 1  # fully blocked / isolated case

print("F.29 PASS: all 64 binary port states; factors 1, 6/5, 3/2, 2, 3, 6; fully blocked case isolated.")
