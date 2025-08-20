from codebank import *
import sys

def main():
    t, = list(read_ints())
    for _ in range(t):
        n, = list(read_ints())
        L = [0]*n; R = [0]*n
        for i in range(n):
            L[i], R[i] = list(read_ints())
        adj = read_tree(n)
        par, depth, order = par_depth_order(adj, 0)
        dp = [[0,0] for _ in range(n)]
        for u in reversed(order):
            p = par[u]
            if p == -1:
                continue
            a0 = dp[u][0] + abs(L[p] - L[u])
            a1 = dp[u][1] + abs(L[p] - R[u])
            dp[p][0] += max(a0, a1)
            b0 = dp[u][0] + abs(R[p] - L[u])
            b1 = dp[u][1] + abs(R[p] - R[u])
            dp[p][1] += max(b0, b1)
        print(max(dp[0]))

if __name__ == "__main__":
    main()