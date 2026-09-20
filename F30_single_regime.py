"""Paper 10.5 — F.30: single-regime falsification harness.

The clean test is deliberately not allowed to pass merely because the measurement
function is hard-coded to the ideal answer. A planted scale-dependent failure must
be rejected by the same harness.
"""

def expected_planar(rho):
    return 4 * rho if rho else 1

def run_harness(measured, rhos, inventories):
    baseline = {(rho, n): expected_planar(rho) for rho in rhos for n in inventories}
    deviations = {(rho, n): measured(rho, n) - baseline[(rho, n)]
                  for rho in rhos for n in inventories}
    # A single-regime failure is a dependence of the deviation on aggregate inventory.
    failure = any(len({deviations[(rho, n)] for n in inventories}) > 1 for rho in rhos)
    return not failure, deviations

rhos = [1, 5, 10, 20, 50]
inventories = [10**3, 10**6, 10**9]

clean_ok, clean_delta = run_harness(lambda rho, n: expected_planar(rho), rhos, inventories)
assert clean_ok
assert all(v == 0 for v in clean_delta.values())

def planted_failure(rho, n):
    return expected_planar(rho) + (0 if n == 10**3 else 1)

failure_ok, failure_delta = run_harness(planted_failure, rhos, inventories)
assert not failure_ok
assert len({failure_delta[(10, n)] for n in inventories}) > 1

print("F.30 PASS: clean rule passes and planted inventory-dependent failure is rejected.")
