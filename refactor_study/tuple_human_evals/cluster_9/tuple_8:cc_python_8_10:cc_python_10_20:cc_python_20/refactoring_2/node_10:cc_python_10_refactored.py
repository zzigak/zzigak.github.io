from codebank import *

def main():
    import sys
    input = sys.stdin.readline
    n, m, s, t = map(int, input().split())
    s -= 1; t -= 1
    adj = [[] for _ in range(n)]
    graph_sets = [set() for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1; v -= 1
        adj[u].append(v)
        adj[v].append(u)
        graph_sets[u].add(v)
        graph_sets[v].add(u)
    ds = bfs_distance(adj, s)
    dt = bfs_distance(adj, t)
    D = ds[t]
    ans = 0
    for u in range(n):
        for v in range(u+1, n):
            if v not in graph_sets[u] and min(ds[u]+dt[v], dt[u]+ds[v]) + 1 >= D:
                ans += 1
    print(ans)

if __name__ == "__main__":
    main()