from codebank import *

def merge_dp(dp_v, dp_u, K, mod):
    size = max(len(dp_v), len(dp_u) + 1)
    res = [0] * size
    for i in range(len(dp_v)):
        for j in range(len(dp_u)):
            prod = dp_v[i] * dp_u[j] % mod
            if i + j + 1 <= K:
                res[max(i, j+1)] = (res[max(i, j+1)] + prod) % mod
            res[i] = (res[i] + prod) % mod
    return res

def main():
    mod = 998244353
    N, K = map(int, input().split())
    adj = read_tree(N)
    par, order = parorder(adj, 0)
    children = get_children(par)
    dp = [[1] for _ in range(N)]
    for u in reversed(order):
        for v in children[u]:
            dp[u] = merge_dp(dp[u], dp[v], K, mod)
    ans = sum(dp[0][i] for i in range(min(K+1, len(dp[0])))) % mod
    print(ans)

if __name__ == "__main__":
    main()