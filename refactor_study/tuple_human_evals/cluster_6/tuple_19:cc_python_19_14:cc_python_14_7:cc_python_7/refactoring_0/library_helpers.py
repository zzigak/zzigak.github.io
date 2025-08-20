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
def falling_factorial(n, k):
    res = 1
    for i in range(k):
        res *= n - i
    return res

def count_sequences(arr, p):
    n = len(arr)
    dp = [[0]*(p+1) for _ in range(n+1)]
    dp[0][0] = 1
    for x in arr:
        for i in range(n-1, -1, -1):
            for s in range(p-x, -1, -1):
                c = dp[i][s]
                if c:
                    dp[i+1][s+x] += c*(i+1)
    counts = [0]*(n+1)
    for i in range(n+1):
        counts[i] = sum(dp[i][s] for s in range(p+1))
    return counts

def build_ladder_jump(board):
    n = 100
    lj = list(range(n))
    for idx in range(n):
        row = idx//10
        col = idx%10 if row%2==0 else 9-(idx%10)
        h = board[row][col]
        if h:
            nr = row - h
            nc = col
            new_idx = nr*10 + (nc if nr%2==0 else 9-nc)
            lj[idx] = new_idx
    return lj

def expected_turns(ladder_jump):
    n = len(ladder_jump)
    E = [0.0]*n
    for i in range(n-2, -1, -1):
        k = min(6, n-1-i)
        s = 0.0
        for d in range(1, k+1):
            j = i+d
            mj = E[ladder_jump[j]] if ladder_jump[j]!=j and E[ladder_jump[j]]<E[j] else E[j]
            s += mj
        E[i] = (6.0 + s)/k
    return E
