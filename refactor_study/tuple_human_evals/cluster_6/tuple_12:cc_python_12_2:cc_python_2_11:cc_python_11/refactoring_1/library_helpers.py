# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return list(map(int, input().split()))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def reduce_frac(num, den):
    g = gcd(num, den)
    return num // g, den // g

def select_top_ops_indices(ops, m):
    return {idx for _, idx in sorted(ops, key=lambda x: x[0], reverse=True)[:m]}

def compute_princess_win_probability(w, b):
    p = [[0.0] * (b + 1) for _ in range(w + 1)]
    for i in range(1, w + 1):
        p[i][0] = 1.0
    for i in range(1, w + 1):
        for j in range(1, b + 1):
            tot = i + j
            prob = i / tot
            if j >= 3:
                prob += (j / tot) * ((j - 1) / (tot - 1)) * ((j - 2) / (tot - 2)) * p[i][j - 3]
            if j >= 2:
                prob += (j / tot) * ((j - 1) / (tot - 1)) * (i / (tot - 2)) * p[i - 1][j - 2]
            p[i][j] = prob
    return p[w][b]
