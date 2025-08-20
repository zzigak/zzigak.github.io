from codebank import *

def main():
    import sys
    input = sys.stdin.buffer.readline
    t = int(input())
    for _ in range(t):
        n = int(input())
        L = [0] * n; R = [0] * n
        for i in range(n):
            L[i], R[i] = map(int, input().split())
        adj = read_tree(n)
        root = 0
        par, order = parorder(adj, root)
        dp = [[0, 0] for _ in range(n)]
        for u in reversed(order[1:]):
            p = par[u]
            merge_dp_interval(dp[p], dp[u], L[p], R[p], L[u], R[u])
        print(max(dp[root]))

if __name__ == "__main__":
    main()