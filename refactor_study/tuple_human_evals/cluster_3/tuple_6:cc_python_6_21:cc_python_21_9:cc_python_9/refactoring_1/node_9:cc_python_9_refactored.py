from codebank import *

def main():
    import sys
    n = int(sys.stdin.readline())
    adj = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = map(int, sys.stdin.readline().split())
        u -= 1; v -= 1
        adj[u].append(v); adj[v].append(u)
    par, order = dfs_order(adj, 0)
    H = [0]*n; F = [0]*n
    for u in order:
        solve_node(u, adj, par, H, F)
    print(H[0])

if __name__ == "__main__":
    main()