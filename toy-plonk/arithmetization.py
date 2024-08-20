from setup import n

def pad_array(a, n):
    return a + [0]*(n - len(a))

# witness vectors
a = [2, 2, 3, 4, 4, 8, -28]
b = [2, 2, 3, 0, 9, 36, 3]
c = [4, 4, 9, 8, 36, -28, -25]

# gate vectors
ql = [0, 0, 0, 2, 0, 1, 1]
qr = [0, 0, 0, 0, 0, -1, 0]
qm = [1, 1, 1, 1, 1, 0, 0]
qc = [0, 0, 0, 0, 0, 0, 3]
qo = [-1, -1, -1, -1, -1, -1, -1]
qpi = [0, 0, 0, 0, 0, 0, 0]

# pad vectors to length n
a = pad_array(a, n)
b = pad_array(b, n)
c = pad_array(c, n)
ql = pad_array(ql, n)
qr = pad_array(qr, n)
qm = pad_array(qm, n)
qc = pad_array(qc, n)
qo = pad_array(qo, n)
qpi = pad_array(qpi, n)

print(f"a = {a}")
print(f"b = {b}")
print(f"c = {c}")
print(f"ql = {ql}")
print(f"qr = {qr}")
print(f"qm = {qm}")
print(f"qc = {qc}")
print(f"qo = {qo}")
print(f"qpi = {qpi}")