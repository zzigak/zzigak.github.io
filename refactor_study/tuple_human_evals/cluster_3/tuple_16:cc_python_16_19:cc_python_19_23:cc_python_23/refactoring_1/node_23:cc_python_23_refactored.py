from codebank import *

def main():
    n, k = read_ints()
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    depth = compute_depths(par, order)
    order2 = sorted(range(n), key=lambda v: depth[v], reverse=True)
    dp = [[1] for _ in range(n)]
    mod = 998244353
    for v in order2:
        p = par[v]
        if p == -1:
            continue
        dp[p] = merge_dp(dp[p], dp[v], k, mod)
    ans = sum(dp[0][i] for i in range(min(k+1, len(dp[0])))) % mod
    print(ans)

if __name__ == "__main__":
    main()