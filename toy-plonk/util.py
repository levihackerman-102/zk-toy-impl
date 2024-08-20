import numpy as np
import galois
from py_ecc.optimized_bls12_381 import add, multiply, G1, G2, neg, pairing, eq, normalize

class SRS:
    def __init__(self, tau, n = 2):
        self.tau = tau
        self.tau1 = [multiply(G1, int(tau)**i) for i in range(0, n + 3)]
        self.tau2 = multiply(G2, int(tau))

    def __str__(self):
        s = f"tau: {self.tau}\n"
        s += "".join([f"[tau^{i}]G1: {str(normalize(point))}\n" for i, point in enumerate(self.tau1)])
        s += f"[tau^{i}]G2: {str(normalize(self.tau2))}\n"
        return s


def new_call(self, at, **kwargs):
    if isinstance(at, SRS):
        coeffs = self.coeffs[::-1]
        result = multiply(at.tau1[0], coeffs[0])
        for i in range(1, len(coeffs)):
            result = add(result, multiply(at.tau1[i], coeffs[i]))
        return result

    return galois.Poly.original_call(self, at, **kwargs)

galois.Poly.original_call = galois.Poly.__call__
galois.Poly.__call__ = new_call
