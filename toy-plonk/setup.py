import galois
import numpy as np
from util import SRS

# Setup

x = 2
y = 3

# 2x^2 - x^2y^2 + 3
out = 2*x**2 - x**2*y**2 + 3
print(f"out = {out}")

# We have 7 gates, next power of 2 is 8
n = 7
n = 2**int(np.ceil(np.log2(n)))
assert n & n - 1 == 0, "n must be a power of 2"

# Prime field p
p = 241
Fp = galois.GF(p)

# Find primitive root of unity
omega = Fp.primitive_root_of_unity(n)
assert omega**(n) == 1, f"omega (ω) {omega} is not a root of unity"

roots = Fp([omega**i for i in range(n)])
print(f"roots = {roots}")

def generate_tau(encrypted=False):
    return SRS(Fp.Random(), n) if encrypted else Fp.Random()

tau = generate_tau()
print(f"--- Tau ---")
print(tau)
