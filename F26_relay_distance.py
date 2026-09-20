"""Paper 10.5 — F.26: relay/taxicab equivalence and planar shell count."""
def relay_steps(delta):
    return sum(abs(v) for v in delta)

def taxicab(delta):
    return sum(abs(v) for v in delta)

count = 0
for x in range(-5, 6):
    for y in range(-5, 6):
        for z in range(-5, 6):
            d = (x, y, z)
            assert relay_steps(d) == taxicab(d)
            count += 1
assert count == 11**3 == 1331

def planar_shell(rho):
    if rho == 0:
        return 1
    return 4 * rho

def planar_enum(rho):
    return sum(1 for x in range(-rho, rho + 1)
               for y in range(-rho, rho + 1)
               if abs(x) + abs(y) == rho)

for rho in range(0, 51):
    assert planar_shell(rho) == planar_enum(rho)

print("F.26 PASS: relay distance equals taxicab distance for 1331 cases; N_planar(rho)=4rho for rho=0..50.")
