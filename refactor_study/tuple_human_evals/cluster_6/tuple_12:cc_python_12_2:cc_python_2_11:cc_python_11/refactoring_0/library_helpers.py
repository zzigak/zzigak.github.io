# ==== RETRIEVED HELPER FUNCTIONS (NONE) ====

# ==== NEW HELPER FUNCTIONS ====
def read_ints():
    return list(map(int, input().split()))

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def reduce_fraction(num, den):
    g = gcd(num, den)
    return num // g, den // g

def print_fraction(num, den):
    n, d = reduce_fraction(num, den)
    print(f"{n}/{d}")

def compute_princess_win_prob(w, b):
    dp = [[0.0] * (b + 1) for _ in range(w + 1)]
    for i in range(1, w + 1):
        dp[i][0] = 1.0
    for i in range(1, w + 1):
        for j in range(1, b + 1):
            total = i + j
            prob = i / total
            if j >= 3:
                prob += (j/total) * ((j-1)/(total-1)) * ((j-2)/(total-2)) * dp[i][j-3]
            if j >= 2:
                prob += (j/total) * ((j-1)/(total-1)) * (i/(total-2)) * dp[i-1][j-2]
            dp[i][j] = prob
    return dp[w][b]

def process_die_probability(x, y):
    z = 7 - max(x, y)
    return reduce_fraction(z, 6)

def best_upgrades(k, a, ops, m):
    groups = [[[], [], []] for _ in range(k)]
    for idx, (t, i, b) in enumerate(ops, 1):
        groups[i-1][t-1].append((b, idx))
    for i in range(k):
        for t in range(3):
            groups[i][t].sort(reverse=True)
    op_list = []
    for i in range(k):
        adds = groups[i][1][:]
        if groups[i][0] and groups[i][0][0][0] > a[i]:
            gain, idx0 = groups[i][0][0][0] - a[i], groups[i][0][0][1]
            adds.append((gain, idx0))
            adds.sort(reverse=True)
        s = a[i]
        for add, idx in adds:
            op_list.append(((s + add)/s, idx))
            s += add
        for mul, idx in groups[i][2]:
            op_list.append((mul, idx))
    op_list.sort(reverse=True)
    selected = set(idx for _, idx in op_list[:m])
    result = []
    for i in range(k):
        for t in range(3):
            for _, idx in groups[i][t]:
                if idx in selected:
                    result.append(idx)
    return result
