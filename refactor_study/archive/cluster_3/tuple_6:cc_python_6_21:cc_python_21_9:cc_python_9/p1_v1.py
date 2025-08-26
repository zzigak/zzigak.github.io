# ########## PROGRAM: node_21:cc_python_21 ##########

from codebank import *

def main():
    import sys
    input = sys.stdin.buffer.readline
    n = int(input())
    beaver = list(map(int, input().split()))
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
    start = int(input()) - 1
    if n == 1:
        print(0)
        return
    order, parent = prune_tree_parents(adj, start)
    dp = [0] * n
    # process leaves inward
    for v in order:
        children = [c for c in adj[v] if parent[c] == v]
        child_dp = sorted((dp[c] for c in children), reverse=True)
        x = min(beaver[v] - 1, len(children))
        if x < 0:
            x = 0
        dp[v] = 1 + sum(child_dp[:x]) + x
        beaver[v] -= x + 1
        for c in children:
            t = min(beaver[v], beaver[c])
            beaver[v] -= t
            dp[v] += 2 * t
    # process root
    children = [c for c in adj[start] if parent[c] == start]
    child_dp = sorted((dp[c] for c in children), reverse=True)
    x = min(beaver[start], len(children))
    if x < 0:
        x = 0
    ans = sum(child_dp[:x]) + x
    beaver[start] -= x
    for c in children:
        t = min(beaver[start], beaver[c])
        beaver[start] -= t
        ans += 2 * t
    print(ans)

if __name__ == "__main__":
    main()