# to prove : we know x,y such that 5*x**3 - 4*x**2*y**2 + 13*x*y**2 + x**2 - 10*y

import galois
import numpy as np

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617 # BN-128
Fp = galois.GF(p)

x = Fp(2)
y = Fp(3)

v1 = x*x
v2 = y*y
v3 = 5*x*v1
v4 = 4*v1*v2
out = 5*x**3 - 4*x**2*y**2 + 13*x*y**2 + x**2 - 10*y

# witness vector
w = Fp([1, out, x, y, v1, v2, v3, v4])
print("w = ", w)

R = Fp([[0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 13, 0, 0, 0, 0, 0]])

L = Fp([[0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0]])

O = Fp([[0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 10, Fp(p - 1), 0, Fp(p - 1), 1]])

Lw = np.dot(L, w)
Rw = np.dot(R, w)
Ow = np.dot(O, w)

print("Lw =", Lw)
print("Rw =", Rw)

LwRw = np.multiply(Lw, Rw)

print("Lw * Rw =", LwRw)
print("Ow =     ", Ow)

assert(np.all(LwRw == Ow))