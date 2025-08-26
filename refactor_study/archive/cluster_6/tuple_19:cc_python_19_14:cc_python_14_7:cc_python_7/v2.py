# ########## LIBRARY HELPERS ##########

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
def build_prefix_dp(arr, max_sum):
    n = len(arr)
    dp = [[[0] * (n + 1) for _ in range(max_sum + 1)] for __ in range(n + 1)]
    for j in range(max_sum + 1):
        for k in range(n + 1):
            dp[0][j][k] = 1
    for i in range(1, n + 1):
        for j in range(max_sum + 1):
            for k in range(1, n + 1):
                dp[i][j][k] = dp[i][j][k - 1]
                a = arr[k - 1]
                if j >= a:
                    dp[i][j][k] += dp[i - 1][j - a][k - 1] * i
    return dp

def compute_expectation_from_prefix_dp(dp, n, p):
    exp_val = 0.0
    fact = n
    for i in range(1, n + 1):
        exp_val += dp[i][p][n] / fact
        fact *= (n - i)
    return exp_val

def count_subsets_by_size_and_sum(arr, max_sum):
    n = len(arr)
    dp = [[0] * (max_sum + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for a in arr:
        for i in range(n - 1, -1, -1):
            for s in range(max_sum, a - 1, -1):
                dp[i + 1][s] += dp[i][s - a]
    return dp

def compute_expected_fail_first(arr, p):
    import math
    n = len(arr)
    fact_n = math.factorial(n)
    ans = 0.0
    for i in range(n):
        arr2 = arr[:i] + arr[i+1:]
        dp2 = count_subsets_by_size_and_sum(arr2, p)
        fk_cache = [math.factorial(k) for k in range(n)]
        for k in range(n):
            fk = fk_cache[k]
            fnk = fk_cache[n - k - 1]
            for s in range(p + 1):
                if s + arr[i] > p:
                    cnt = dp2[k][s] * fk * fnk
                    ans += k * cnt
    return ans / fact_n

def generate_path_mappings():
    Y = [(i // 10, 9 - i % 10 if (i // 10) & 1 else i % 10) for i in range(100)]
    Z = [[i * 10 + (9 - j if i & 1 else j) for j in range(10)] for i in range(10)]
    return Y, Z

def build_ladder_jump(ladders, Y, Z):
    jump = [0] * 100
    for idx, (x, y) in enumerate(Y):
        h = ladders[x][y]
        if h:
            tx = x - h
            jump[idx] = Z[tx][y]
    return jump

def expected_turns(jump):
    E = [0.0] * 100
    for i in range(1, 6):
        E[i] = (sum(E[:i]) + 6) / i
    for i in range(6, 100):
        E[i] = sum(E[i-6:i]) / 6 + 1
        j = jump[i]
        if j:
            E[i] = min(E[i], E[j])
    return E[99]


# ########################################
#
#  PROGRAM REFACTORINGS
#
# ########################################

# ########## PROGRAM: node_14:cc_python_14 ##########

from codebank import count_subsets_by_size_and_sum, compute_expected_fail_first

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1+n]))
    p = int(data[1+n])
    if sum(a) <= p:
        print(n)
    else:
        print(compute_expected_fail_first(a, p))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import build_prefix_dp, compute_expectation_from_prefix_dp

def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    arr = list(map(int, data[1:1+n]))
    p = int(data[1+n])
    dp = build_prefix_dp(arr, p)
    print(compute_expectation_from_prefix_dp(dp, n, p))

if __name__ == "__main__":
    main()

# ########## PROGRAM: node_7:cc_python_7 ##########

from codebank import generate_path_mappings, build_ladder_jump, expected_turns

def main():
    import sys
    ladders = [list(map(int, sys.stdin.readline().split())) for _ in range(10)]
    Y, Z = generate_path_mappings()
    jump = build_ladder_jump(ladders, Y, Z)
    print(expected_turns(jump))

if __name__ == "__main__":
    main()
