# ########## PROGRAM: node_19:cc_python_19 ##########

from codebank import *

def solve_case():
    n = int(input())
    L = [0] * n; R = [0] * n
    for i in range(n):
        L[i], R[i] = map(int, input().split())
    adj = read_tree(n)
    par, order = parorder(adj, 0)
    dp = [[0, 0] for _ in range(n)]
    for u in reversed(order):
        dp[u] = [0, 0]
        for v in adj[u]:
            if v == par[u]: continue
            dp0 = max(dp[v][0] + abs(L[u] - L[v]),
                      dp[v][1] + abs(L[u] - R[v]))
            dp1 = max(dp[v][0] + abs(R[u] - L[v]),
                      dp[v][1] + abs(R[u] - R[v]))
            dp[u][0] += dp0
            dp[u][1] += dp1
    return max(dp[0])

def main():
    t = int(input())
    for _ in range(t):
        print(solve_case())

if __name__ == "__main__":
    main()