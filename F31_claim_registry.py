"""Paper 10.5 — F.31: claim-graph / bridge-ledger registry audit."""
import re

AXIOMS = {"L1", "L2", "L3", "L4", "PTR", "BUDGET", "S3"}
DEFERRED = {"P10", "P13", "P14", "P16", "P23", "P24"}
LEVELS = {"A", "B", "C"}
FORBIDDEN_NATIVE = {"metric", "tensor", "field", "curvature", "manifold", "vacuum", "geodesic", "integral", "continuum"}

REGISTRY = [
    {"id":"SHELL_COUNT", "level":"A", "axioms":["L1","L2","L3","L4"], "deps":[], "deferred":[], "script":"F.2", "obs":False, "text":"exact integer shell count"},
    {"id":"BETA_UNIQUE", "level":"A", "axioms":["L1","L2","L3","S3"], "deps":[], "deferred":[], "script":"F.25", "obs":False, "text":"beta = one third from three axes and conservation"},
    {"id":"RELAY_EQUIVALENCE", "level":"A", "axioms":["L2","L3"], "deps":[], "deferred":[], "script":"F.26", "obs":False, "text":"integer relay distance equals taxicab distance"},
    {"id":"MASS_QUANTUM", "level":"A", "axioms":["BUDGET"], "deps":[], "deferred":[], "script":"F.27", "obs":False, "text":"minimum non-zero workload is one CU"},
    {"id":"TWO_TRANSITIONS", "level":"A", "axioms":["PTR"], "deps":[], "deferred":[], "script":"F.28", "obs":False, "text":"two mandatory internal operations"},
    {"id":"PORT_EXHAUSTION", "level":"A", "axioms":["BUDGET"], "deps":[], "deferred":[], "script":"F.29", "obs":False, "text":"six-port finite blocking enumeration"},
    {"id":"SINGLE_REGIME_HARNESS", "level":"A", "axioms":["L1","L2","L3"], "deps":[], "deferred":[], "script":"F.30", "obs":False, "text":"finite falsification harness"},
    {"id":"PHYSICAL_RECONSTRUCTION", "level":"B", "axioms":[], "deps":["SHELL_COUNT"], "deferred":["P16"], "script":"F.4", "obs":False, "text":"physical reconstruction shadow"},
    {"id":"OBSERVATIONAL_TEST", "level":"C", "axioms":[], "deps":["PHYSICAL_RECONSTRUCTION"], "deferred":[], "script":"F.obs", "obs":True, "text":"observational protocol"},
]

def acyclic(reg):
    graph = {r['id']: set(r['deps']) for r in reg}
    visiting, done = set(), set()
    def visit(n):
        if n in visiting: return False
        if n in done: return True
        visiting.add(n)
        for d in graph.get(n, set()):
            if d not in graph or not visit(d): return False
        visiting.remove(n); done.add(n); return True
    return all(visit(n) for n in graph)

def audit(reg):
    ids = [r['id'] for r in reg]
    assert len(ids) == len(set(ids))
    assert acyclic(reg)
    for r in reg:
        assert r['level'] in LEVELS
        assert r['script']
        assert all(a in AXIOMS for a in r['axioms'])
        assert all(d in DEFERRED for d in r['deferred'])
        if r['obs']:
            assert r['level'] in {'B','C'}
        if r['level'] == 'A':
            assert not r['deferred']
        assert r['text']
        words = set(re.findall(r'\b[a-z]+\b', r['text'].lower()))
        assert not (words & FORBIDDEN_NATIVE)
    return True

assert audit(REGISTRY)

# R1–R10 poisoned-registry tests.
def poisoned(base, mutation):
    import copy
    r = copy.deepcopy(base)
    mutation(r)
    return r

poisons = [
    lambda r: r.__setitem__(0, {**r[0], 'id':'SHELL_COUNT', 'level':'A', 'deferred':['P16']}),
    lambda r: r.__setitem__(1, {**r[1], 'obs':True, 'level':'A'}),
    lambda r: r.__setitem__(2, {**r[2], 'deps':['MISSING']}),
    lambda r: r.__setitem__(3, {**r[3], 'axioms':['UNKNOWN']}),
    lambda r: r.__setitem__(4, {**r[4], 'script':''}),
    lambda r: r.append({**r[0], 'id':'SHELL_COUNT'}),
    lambda r: r.__setitem__(5, {**r[5], 'deferred':['UNKNOWN_TARGET']}),
    lambda r: r.__setitem__(6, {**r[6], 'level':'Z'}),
    lambda r: r.__setitem__(7, {**r[7], 'text':'continuum metric leakage'}),
    lambda r: (r.__setitem__(0, {**r[0], 'deps':['OBSERVATIONAL_TEST']}), r.__setitem__(8, {**r[8], 'deps':['SHELL_COUNT']})),
]
for mutation in poisons:
    try:
        audit(poisoned(REGISTRY, mutation))
    except (AssertionError, RecursionError):
        pass
    else:
        raise AssertionError('Poisoned registry was not rejected')

print("F.31 PASS: clean registry accepted; ten planted breach classes rejected.")
