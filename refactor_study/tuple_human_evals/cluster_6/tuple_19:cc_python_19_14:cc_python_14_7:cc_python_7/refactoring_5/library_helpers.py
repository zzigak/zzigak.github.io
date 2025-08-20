# ==== RETRIEVED HELPER FUNCTIONS ====
def build_pair_dp(maxn, mod):
    # Success rate: 1/1

    inv2 = modinv(2, mod)
    dp = [[0] * (maxn + 1) for _ in range(maxn + 1)]
    for u in range(1, maxn + 1):
        dp[u][0] = 1
    for u in range(1, maxn + 1):
        for v in range(1, maxn + 1):
            dp[u][v] = (dp[u - 1][v] + dp[u][v - 1]) * inv2 % mod
    return dp

def survival_probability(a, b, c, dp):
    # Success rate: 1/1

    if a == 0 or b == 0:
        return 0.0
    if c == 0:
        return 1.0
    div = a * b + b * c + c * a
    return a * b / div * dp[a][b - 1][c] + b * c / div * dp[a][b][c - 1] + a * c / div * dp[a - 1][b][c]

def compute_probabilities(dist_sq_list, R2):
    # Success rate: 1/1

    return [1.0 if d <= R2 else math.exp(1 - d / R2) for d in dist_sq_list]

def subset_sum_dp(weights, max_sum, mod):
    # Success rate: 1/1

    dp = [0] * (max_sum + 1)
    dp[0] = 1
    for w in weights:
        for s in range(max_sum, w - 1, -1):
            dp[s] = (dp[s] + dp[s - w]) % mod
    return dp

def dp_likes_distribution(li, di, m, mod):
    # Success rate: 0.0/0
    SU = li + di
    dp = [1] + [0] * m
    SU_mod = SU % mod
    inv = [0] * (2 * m + 1)
    for x in range(-m, m + 1):
        inv[x + m] = pow(SU_mod + x, mod - 2, mod)
    for t in range(m):
        dp2 = [0] * (m + 1)
        for k in range(t + 1):
            inv_tot = inv[2 * k - t + m]
            base = dp[k] * inv_tot % mod
            wl = li + k
            bd = di - (t - k)
            dp2[k] = (dp2[k] + base * wl) % mod
            dp2[k + 1] = (dp2[k + 1] + base * bd) % mod
        dp = dp2
    return dp

def knapsack_one_per_type(counts, mod):
    # Success rate: 1/1

    m = len(counts)
    dp = [1] + [0] * m
    for c in counts:
        for j in range(m, 0, -1):
            dp[j] = (dp[j] + dp[j - 1] * c) % mod
    return dp

def get_princess_win_prob(w, b):
    # Success rate: 1/1

    dp = create_2d_list(w + 1, b + 1, 0.0)
    for i in range(1, w + 1):
        dp[i][0] = 1.0
    for i in range(1, w + 1):
        for j in range(1, b + 1):
            total = i + j
            res = i / total
            if j >= 3:
                res += j / total * ((j - 1) / (total - 1)) * ((j - 2) / (total - 2)) * dp[i][j - 3]
            if j >= 2:
                res += j / total * ((j - 1) / (total - 1)) * (i / (total - 2)) * dp[i - 1][j - 2]
            dp[i][j] = res
    return dp[w][b]

def factorial_inverses(n, mod):
    # Success rate: 4/4

    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % mod
    invfact = [1] * (n + 1)
    invfact[n] = pow(fact[n], mod - 2, mod)
    for i in range(n - 1, -1, -1):
        invfact[i] = invfact[i + 1] * (i + 1) % mod
    return (fact, invfact)


# ==== NEW HELPER FUNCTIONS ====
def permutation_counts(sizes, max_sum):
    n = len(sizes)
    dp = [[0] * (max_sum + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for a in sizes:
        ndp = [row.copy() for row in dp]
        for i in range(n):
            coef = i + 1
            for s in range(max_sum + 1 - a):
                val = dp[i][s]
                if val:
                    ndp[i + 1][s + a] += coef * val
        dp = ndp
    return dp

def factorial_list(n):
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i
    return fact

def build_mappings(rows=10, cols=10):
    Y = [(i // cols, cols - 1 - i % cols if (i // cols) & 1 else i % cols)
         for i in range(rows * cols)]
    Z = [[0] * cols for _ in range(rows)]
    for x in range(rows):
        for y in range(cols):
            Z[x][y] = x * cols + (cols - 1 - y if x & 1 else y)
    return Y, Z

def build_ladder_mapping(X):
    Y, Z = build_mappings()
    L = [None] * len(Y)
    for i, (x, y) in enumerate(Y):
        h = X[x][y]
        if h:
            L[i] = Z[x - h][y]
    return L

def expected_turns(X, dice_sides=6):
    L = build_ladder_mapping(X)
    n = len(L)
    E = [0.0] * n
    F = [0.0] * n
    for i in range(1, dice_sides):
        F[i] = E[i] = (sum(E[:i]) + dice_sides) / i
    for i in range(dice_sides, n):
        F[i] = E[i] = sum(F[i - dice_sides:i]) / dice_sides + 1
        tgt = L[i]
        if tgt is not None:
            F[i] = min(E[i], E[tgt])
    return F[n - 1]
