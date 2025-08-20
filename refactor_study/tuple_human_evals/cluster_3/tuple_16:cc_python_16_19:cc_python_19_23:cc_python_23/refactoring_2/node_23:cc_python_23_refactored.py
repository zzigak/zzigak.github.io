from codebank import *
import sys

def main():
    n, K = list(read_ints())
    adj = read_tree(n)
    par, depth, order = par_depth_order(adj, 0)
    dp = [[1] for _ in range(n)]
    for u in reversed(order):
        p = par[u]
        if p != -1:
            dp[p] = merge_dp(dp[p], dp[u], K)
    ans = sum(dp[0][i] for i in range(min(K+1, len(dp[0])))) % 998244353
    print(ans)

if __name__ == "__main__":
    main()