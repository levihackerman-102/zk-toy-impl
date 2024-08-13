# to prove : we know x,y such that 5*x**3 - 4*x**2*y**2 + 13*x*y**2 + x**2 - 10*y

import galois
import numpy as np

p = 21888242871839275222246405745257275088548364400416034343698204186575808495617 # BN-128
# p = 71
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

mats = [L, R, O]
poly_m = []

for m in mats:
    poly_list = []
    for i in range(0, m.shape[1]):
        points_x = Fp(np.zeros(m.shape[0], dtype=int))
        points_y = Fp(np.zeros(m.shape[0], dtype=int))
        for j in range(0, m.shape[0]):
            points_x[j] = Fp(j+1)
            points_y[j] = m[j][i]

        poly = galois.lagrange_poly(points_x, points_y)
        coef = poly.coefficients()[::-1]
        if len(coef) < m.shape[0]:
            coef = np.append(coef, np.zeros(m.shape[0] - len(coef), dtype=int))
        poly_list.append(coef)
    
    poly_m.append(Fp(poly_list))

Lp = poly_m[0]
Rp = poly_m[1]
Op = poly_m[2]

print(f'''Lp
{Lp}
''')

print(f'''Rp
{Rp}
''')

print(f'''Op
{Op}
''')

U = galois.Poly((w @ Lp)[::-1])
V = galois.Poly((w @ Rp)[::-1])
W = galois.Poly((w @ Op)[::-1])

print("U = ", U)
print("V = ", V)
print("W = ", W)

tau = Fp(20)

print(f"τ = {tau}")

T = galois.Poly([1, p-1], field=Fp)
for i in range(2, L.shape[0] + 1):
    T *= galois.Poly([1, p-i], field=Fp)

print("\nT = ", T)
for i in range(1, L.shape[0] + 2):
    print(f"T({i}) = ", T(i))
    if i == L.shape[0]:
        print("-"*10)

T_tau = T(tau)
print(f"\nT(τ) = {T_tau}")

H = (U * V - W) // T
rem = (U * V - W) % T

print("H = ", H)
print("rem = ", rem)

assert(rem == 0)

u = U(tau)
v = V(tau)
_w = W(tau)
ht = H(tau)*T_tau

assert u * v - _w == ht, f"{u} * {v} - {_w} != {ht}" # this equation should hold