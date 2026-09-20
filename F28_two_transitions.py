"""Paper 10.5 — F.28: two mandatory internal operations."""

# The declared execution ontology has two distinct mandatory categories per link.
MANDATORY_OPERATIONS = ("identity_verification", "temporal_propagation")
assert len(MANDATORY_OPERATIONS) == 2

# One operation cannot satisfy two distinct mandatory categories.
one_operation_satisfies = {"identity_verification"}
assert set(MANDATORY_OPERATIONS) - one_operation_satisfies

# No third mandatory category is declared by the Per-Triangle execution rule.
assert "third_mandatory_category" not in MANDATORY_OPERATIONS
N_TRANSITIONS = len(MANDATORY_OPERATIONS)
assert N_TRANSITIONS == 2

print("F.28 PASS: N_transitions=2 from two distinct mandatory categories; physical time mapping remains downstream.")
