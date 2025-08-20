from codebank import *

def main():
    import sys
    input = sys.stdin.buffer.readline
    mod = 998244353
    n, K = map(int, input().split())
    adj = read_tree(n)
    root = 0
    par, order = parorder(adj, root)
    dp = [[1] for _ in range(n)]
    for u in reversed(order[1:]):
        p = par[u]
        dp[p] = merge_dp_diameter(dp[p], dp[u], K, mod)
    ans = sum(dp[root][i] for i in range(min(K + 1, len(dp[root])))) % mod
    print(ans)

if __name__ == "__main__":
    main()