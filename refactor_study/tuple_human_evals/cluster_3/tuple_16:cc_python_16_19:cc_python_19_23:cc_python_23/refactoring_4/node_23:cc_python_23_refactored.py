from codebank import *

def main():
    mod = 998244353
    n, K = map(int, input().split())
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    children = get_children(par)
    dp = [[1] for _ in range(n)]
    for u in reversed(order):
        for c in children[u]:
            dp[u] = merge_dp(dp[u], dp[c], K, mod)
    print(sum(dp[0][:K+1]) % mod)

if __name__ == "__main__":
    main()