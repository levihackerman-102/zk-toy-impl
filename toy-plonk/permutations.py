import numpy as np
from setup import n, roots, Fp
from arithmetization import a, b, c

def print_sigma(sigma, a, b, c, r):
    group_size = len(sigma) // 3
    padding = 6

    print(f"{' w'} | {'value':{padding}} | {'i':{padding}} | {'sigma(i)':{padding}}")

    for i in range(0, group_size):
        print(f"a{i} | {a[i]:{padding}} | {r[i]:{padding}} | {r[sigma[i]]:{padding}}")

    print(f"-- | {'--':{padding}} | {'--':{padding}} | {'--':{padding}}")

    for i in range(group_size, 2 * group_size):
        print(f"b{i - group_size} | {b[i - group_size]:{padding}} | {r[i]:{padding}} | {r[sigma[i]]:{padding}}")

    print(f"-- | {'--':{padding}} | {'--':{padding}} | {'--':{padding}}")

    for i in range(2 * group_size, 3 * group_size):
        print(f"c{i - 2 * group_size} | {c[i - 2 * group_size]:{padding}} | {r[i]:{padding}} | {r[sigma[i]]:{padding}}")

ai = range(0, n)
bi = range(n, 2*n)
ci = range(2*n, 3*n)

sigma = {
    ai[0]: ai[0], ai[1]: ai[1], ai[2]: ai[2], ai[3]: ci[0], ai[4]: ci[1], ai[5]: ci[3], ai[6]: ci[5], ai[7]: ai[7],
    bi[0]: bi[0], bi[1]: bi[1], bi[2]: bi[2], bi[3]: bi[3], bi[4]: ci[2], bi[5]: ci[4], bi[6]: bi[6], bi[7]: bi[7],
    ci[0]: ai[3], ci[1]: ai[4], ci[2]: bi[4], ci[3]: ai[5], ci[4]: bi[5], ci[5]: ai[6], ci[6]: ci[6], ci[7]: ci[7],
}

k1 = 2
k2 = 4
c1_roots = roots
c2_roots = roots * k1
c3_roots = roots * k2

c_roots = np.concatenate((c1_roots, c2_roots, c3_roots))

check = set()
for r in c_roots:
    assert not int(r) in check, f"Duplicate root {r} in {c_roots}"
    check.add(int(r))

sigma1 = Fp([c_roots[sigma[i]] for i in range(0, n)])
sigma2 = Fp([c_roots[sigma[i + n]] for i in range(0, n)])
sigma3 = Fp([c_roots[sigma[i + 2 * n]] for i in range(0, n)])

print_sigma(sigma, a, b, c, c_roots)

print("\n\n--- Cosest ---")
print(f"c0 = {c1_roots}")
print(f"c1 = {c2_roots}")
print(f"c2 = {c3_roots}")

print("\n\n--- Sigma ---")
print(f"sigma1 = {sigma1}")
print(f"sigma2 = {sigma2}")
print(f"sigma3 = {sigma3}")