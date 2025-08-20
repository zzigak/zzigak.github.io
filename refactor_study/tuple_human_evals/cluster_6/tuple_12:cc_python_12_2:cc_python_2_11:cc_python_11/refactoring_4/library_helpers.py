# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def reduce_fraction(n, d):
    g = gcd(n, d)
    return n // g, d // g

def compute_princess_prob(w, b):
    p = [[0.0] * (b + 1) for _ in range(w + 1)]
    for i in range(1, w + 1):
        p[i][0] = 1.0
    for i in range(1, w + 1):
        for j in range(1, b + 1):
            t = i / (i + j)
            if j >= 3:
                t += (j / (i + j)) * ((j - 1) / (i + j - 1)) * ((j - 2) / (i + j - 2)) * p[i][j - 3]
            if j >= 2:
                t += (j / (i + j)) * ((j - 1) / (i + j - 1)) * (i / (i + j - 2)) * p[i - 1][j - 2]
            p[i][j] = t
    return p[w][b]

def get_skill_ops(a_i, assigns, adds, muls):
    ops = []
    if assigns:
        b0, idx0 = max(assigns)
        gain0 = b0 - a_i
    else:
        gain0 = 0
    t = adds.copy()
    if gain0 > 0:
        t.append((gain0, idx0))
    t.sort(reverse=True)
    s = a_i
    for gain, idx in t:
        ratio = (s + gain) / s
        ops.append((ratio, idx))
        s += gain
    for mul, idx in sorted(muls, reverse=True):
        ops.append((mul, idx))
    return ops
