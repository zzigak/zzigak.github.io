from codebank import *

def main():
    n = int(input())
    colors = list(map(int, input().split()))
    adj = read_tree(n, offset=1)
    # build weight: +1 white, -1 black
    w = [0] * (n + 1)
    for i in range(1, n + 1):
        w[i] = 1 if colors[i - 1] == 1 else -1
    par, order = parorder(adj, 1)
    # initial DP on rooted tree
    dp = [0] * (n + 1)
    for u in reversed(order):
        dp[u] = w[u]
        for v in adj[u]:
            if v != par[u]:
                dp[u] += max(dp[v], 0)
    # reroot DP to get answer for each vertex
    dp2 = [0] * (n + 1)
    dp2[1] = dp[1]
    for u in order:
        for v in adj[u]:
            if v != par[u]:
                dp2[v] = dp[v] + max(dp2[u] - max(dp[v], 0), 0)
    print(*(dp2[1:]))

if __name__ == "__main__":
    main()