from codebank import *

def main():
    import sys
    sys.setrecursionlimit(10**7)
    n = int(input())
    w = list(map(int, input().split()))
    adj = read_weighted_tree(n)
    parent, order = get_postorder(adj, 0)
    dp = [0] * n
    ans = 0
    for u in order:
        contrib = []
        for v_c in adj[u]:
            v, c = v_c
            if v != parent[u]:
                contrib.append(dp[v] - c)
        contrib.sort(reverse=True)
        best = contrib[0] if contrib and contrib[0] > 0 else 0
        dp[u] = w[u] + best
        if dp[u] > ans:
            ans = dp[u]
        if len(contrib) >= 2 and contrib[1] > 0:
            val = w[u] + contrib[0] + contrib[1]
            if val > ans:
                ans = val
    print(ans)

if __name__ == "__main__":
    main()