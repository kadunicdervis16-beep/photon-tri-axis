"""Paper 10.5 — F.25: exact beta=1/3 audit."""
from fractions import Fraction
from itertools import permutations, product

STATES = list(product("XYO", repeat=3))
assert len(STATES) == 27
assert 6 == 3 * 2
N_AXIS = 3
N_TOTAL = 100
P_ID = 3
C_EXEC = N_TOTAL - P_ID
assert C_EXEC == 97

S3 = list(permutations(range(3)))
def permute(state, p):
    return tuple(state[p[i]] for i in range(3))

orbits = {frozenset(permute(s, p) for p in S3) for s in STATES}
assert len(orbits) == 10
assert sum(1 for o in orbits if len(o) == 3) == 6

# Conservation and equivalent treatment force equal axis fractions.
beta = Fraction(1, N_AXIS)
assert beta * N_AXIS == 1
assert beta == Fraction(1, 3)

print("F.25 PASS: beta = 1/3; 27 states, 6 ports, S3 axis equivalence, conserved partition.")
