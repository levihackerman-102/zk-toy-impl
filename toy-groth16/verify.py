import galois
from qap import p, T, U, V, W, H

Fp = galois.GF(p)

print("Setup phase")
print("-"*10)
print("Toxic waste:")
tau = Fp(20)

print(f"τ = {tau}")

T_tau = T(tau)
print(f"\nT(τ) = {T_tau}")

# ...
from py_ecc.optimized_bn128 import multiply, G1, G2, add, pairing, neg, normalize

# G1[τ^0], G1[τ^1], ..., G1[τ^d]
tau_G1 = [multiply(G1, int(tau**i)) for i in range(0, T.degree)]
# G1[τ^0 * T(τ)], G1[τ^1 * T(τ)], ..., G1[τ^d-1 * T(τ)]
target_G1 = [multiply(G1, int(tau**i * T_tau)) for i in range(0, T.degree - 1)]

# G2[τ^0], G2[τ^1], ..., G2[τ^d]
tau_G2 = [multiply(G2, int(tau**i)) for i in range(0, T.degree)]

print("Trusted setup:")
print("-"*10)
print(f"[τ]G1 = {[normalize(point) for point in tau_G1]}")
print(f"[T(τ)]G1 = {[normalize(point) for point in target_G1]}")

print(f"\n[τ]G2 = {[normalize(point) for point in tau_G2]}")

def evaluate_poly(poly, trusted_points, verbose=False):
    coeff = poly.coefficients()[::-1]

    assert len(coeff) == len(trusted_points), "Polynomial degree mismatch!"

    if verbose:
        [print(normalize(point)) for point in trusted_points]

    terms = [multiply(point, int(coeff)) for point, coeff in zip(trusted_points, coeff)]
    evaluation = terms[0]
    for i in range(1, len(terms)):
        evaluation = add(evaluation, terms[i])

    if verbose:
        print("-"*10)
        print(normalize(evaluation))
    return evaluation

print("\nProof generation:")
print("-"*10)
# G1[u0 * τ^0] + G1[u1 * τ^1] + ... + G1[ud-1 * τ^d-1]
A_G1 = evaluate_poly(U, tau_G1)
# G2[v0 * τ^0] + G2[v1 * τ^1] + ... + G2[vd-1 * τ^d-1]
B_G2 = evaluate_poly(V, tau_G2)
# G1[w0 * τ^0] + G1[w1 * τ^1] + ... + G1[wd-1 * τ^d-1]
B_G1 = evaluate_poly(V, tau_G1)
# G1[w0 * τ^0] + G1[w1 * τ^1] + ... + G1[wd-1 * τ^d-1]
Cw_G1 = evaluate_poly(W, tau_G1)
# G1[h0 * τ^0 * T(τ)] + G1[h1 * τ^1 * T(τ)] + ... + G1[hd-2 * τ^d-2 * T(τ)]
HT_G1 = evaluate_poly(H, target_G1)

C_G1 = add(Cw_G1, HT_G1)

print(f"[A]G1 = {normalize(A_G1)}")
print(f"[B]G2 = {normalize(B_G2)}")
print(f"[C]G1 = {normalize(C_G1)}")

print("\nProof verification:")
print("-"*10)
# e(A, B) == e(C, G2[1])
assert pairing(B_G2, A_G1) == pairing(G2, C_G1), "Pairing check failed!"
print("Pairing check passed!")